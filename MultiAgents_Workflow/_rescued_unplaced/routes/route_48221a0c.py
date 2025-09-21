from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
import json
import uuid
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Profile, Log
from .auth import get_current_user
from ..routes.research_adapter import _thread_cfg

# Import the research graph
import sys
from pathlib import Path

agent_dir = Path(__file__).parent.parent.parent / "agents" / "ResearchAgent" / "graph"
sys.path.insert(0, str(agent_dir.parent.parent))

try:
    from agents.ResearchAgent.graph.graph_main import graph as research_graph
except ImportError:
    # Fallback for different environments
    from ...agents.ResearchAgent.graph.graph_main import graph as research_graph

from ..models import Profile

router = APIRouter(tags=["Frontend API"])

class AgentRequest(BaseModel):
    topic: str
    max_analysts: int = 2
    session_id: str = None

class AgentResponse(BaseModel):
    session_id: str
    status: str
    message: str

@router.post("/run-research", response_model=AgentResponse)
async def run_research_agent(
    request: AgentRequest,
    current_user: Profile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trigger research agent execution (streaming happens separately)"""
    try:
        # Generate session ID
        session_id = request.session_id or str(uuid.uuid4())

        # Log the agent execution start
        db_log = Log(
            user_id=current_user.id,
            agent="research-agent",
            stage="start",
            message=f"Research triggered for topic: {request.topic}"
        )
        db.add(db_log)
        db.commit()

        # Don't run research here - let streaming endpoint handle it
        # Just return success immediately so frontend can start streaming
        return AgentResponse(
            session_id=session_id,
            status="started",
            message=f"Research started for topic: {request.topic}. Connecting to live stream..."
        )

    except Exception as e:
        # Log error
        error_log = Log(
            user_id=current_user.id,
            agent="research-agent",
            stage="error",
            message=f"Failed to start research: {str(e)}"
        )
        db.add(error_log)
        db.commit()

        raise HTTPException(status_code=500, detail=f"Failed to start research: {str(e)}")

@router.get("/research-stream")
async def stream_research(
    request: Request,
    topic: str,
    max_analysts: int = 2,
    token: str = None,  # Accept token as URL parameter
    db: Session = Depends(get_db)
):
    """Stream research agent execution in real-time"""
    session_id = str(uuid.uuid4())

    # Validate token and get user
    if not token:
        error_data = {"type": "error", "error": "No authentication token provided"}
        async def error_generate():
            yield f"data: {json.dumps(error_data)}\n\n".encode()
        return StreamingResponse(error_generate(), media_type="text/event-stream")

    try:
        from .auth import SECRET_KEY, ALGORITHM, jwt
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Invalid token")
        user = db.query(Profile).filter(Profile.email == email).first()
        if user is None:
            raise ValueError("User not found")
    except Exception:
        error_data = {"type": "error", "error": "Invalid authentication token"}
        async def error_generate():
            yield f"data: {json.dumps(error_data)}\n\n".encode()
        return StreamingResponse(error_generate(), media_type="text/event-stream")

    async def generate() -> AsyncGenerator[bytes, None]:
        stored_results = {}  # Store final results as they become available

        try:
            # Log start
            yield f"data: {json.dumps({'type': 'start', 'session_id': session_id, 'topic': topic})}\n\n".encode()

            # Prepare payload with user-specified parameters
            payload = {
                "topic": topic,
                "max_analysts": max_analysts,
                "human_analyst_feedback": "continue"
            }

            # Stream events from the research graph
            async for event in research_graph.astream_events(payload, _thread_cfg(session_id)):
                # Convert event data to JSON-serializable format
                event_data = {
                    "type": "event",
                    "event": event.get("event"),
                    "name": event.get("name", ""),
                    "data": str(event.get("data", {})),  # Convert to string to avoid JSON issues
                    "tags": list(event.get("tags", [])) if event.get("tags") else [],
                    "timestamp": str(event.get("timestamp")) if event.get("timestamp") else ""
                }
                yield f"data: {json.dumps(event_data)}\n\n".encode()

                # Capture final results as they become available
                if event.get("name") == "finalize_report":
                    try:
                        event_values = event.get("data", {})
                        print(f"DEBUG: finalize_report event data keys: {list(event_values.keys()) if isinstance(event_values, dict) else 'not dict'}", file=sys.stderr)

                        final_report = None

                        if isinstance(event_values, dict):
                            # Check for final_report in nested output structure (most common)
                            if 'output' in event_values and isinstance(event_values['output'], dict):
                                if 'final_report' in event_values['output']:
                                    final_report = event_values['output']['final_report']
                                    print(f"Found final_report in output", file=sys.stderr)
                            # Also check root level
                            elif 'final_report' in event_values:
                                final_report = event_values['final_report']
                                print(f"Found final_report in root level", file=sys.stderr)
                            # Check chunk level
                            elif 'chunk' in event_values and isinstance(event_values['chunk'], dict):
                                if 'final_report' in event_values['chunk']:
                                    final_report = event_values['chunk']['final_report']
                                    print(f"Found final_report in chunk", file=sys.stderr)

                        if final_report:
                            stored_results = {
                                'topic': payload.get('topic', topic),
                                'final_report': final_report,
                                'introduction': '',  # Will be extracted from final_report if needed
                                'conclusion': '',    # Will be extracted from final_report if needed
                                'sections': [],      # Not available in final_report return
                                'analysts': []       # Not available in final_report return
                            }
                            print(f"CAPTURED FINAL RESULTS: {len(final_report)} chars", file=sys.stderr)
                            print(f"SAMPLE: {final_report[:200]}...", file=sys.stderr)
                        else:
                            print(f"NO final_report found in any location", file=sys.stderr)
                    except Exception as capture_error:
                        print(f"Failed to capture results: {capture_error}", file=sys.stderr)
                        import traceback
                        print(f"Traceback: {traceback.format_exc()}", file=sys.stderr)

                # Log important events
                if event.get("event") == "end":
                    log_entry = Log(
                        user_id=user.id,
                        agent="research-agent",
                        stage="stream_complete",
                        message=f"Stream completed for topic: {topic}"
                    )
                    db.add(log_entry)
                    db.commit()

                    # Final fallback: try to get results from the graph state at the end
                    if not stored_results:
                        try:
                            print(f"FINAL FALLBACK: Attempting to get results from graph state", file=sys.stderr)
                            config = {"configurable": {"thread_id": session_id}}
                            final_state = research_graph.get_state(config)
                            if final_state and 'values' in final_state:
                                state_values = final_state['values']
                                print(f"FINAL FALLBACK: State keys: {list(state_values.keys())}", file=sys.stderr)
                                stored_results = {
                                    'topic': state_values.get('topic', topic),
                                    'final_report': state_values.get('final_report', ''),
                                    'introduction': state_values.get('introduction', ''),
                                    'conclusion': state_values.get('conclusion', ''),
                                    'sections': state_values.get('sections', []),
                                    'analysts': state_values.get('analysts', [])
                                }
                                print(f"FINAL FALLBACK: Captured {len(stored_results.get('final_report', ''))} chars", file=sys.stderr)
                        except Exception as fallback_error:
                            print(f"FINAL FALLBACK failed: {fallback_error}", file=sys.stderr)

            # Send completion event with results
            completion_data = {
                "type": "complete",
                "session_id": session_id,
                "message": "Research completed successfully",
                "results": stored_results if stored_results else {
                    'topic': topic,
                    'final_report': 'Research completed successfully. Results will be available shortly.',
                    'introduction': '',
                    'conclusion': '',
                    'sections': [],
                    'analysts': []
                }
            }
            print(f"SENDING COMPLETION EVENT WITH RESULTS: {len(stored_results.get('final_report', '')) if stored_results else 0} chars", file=sys.stderr)
            yield f"data: {json.dumps(completion_data, ensure_ascii=False)}\n\n".encode()

        except Exception as e:
            error_data = {
                "type": "error",
                "error": str(e),
                "session_id": session_id
            }
            yield f"data: {json.dumps(error_data)}\n\n".encode()

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@router.get("/user-sessions")
async def get_user_sessions(
    current_user: Profile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's research sessions and logs"""
    logs = db.query(Log).filter(Log.user_id == current_user.id).order_by(Log.created_at.desc()).limit(50).all()

    sessions = {}
    for log in logs:
        session_key = f"{log.agent}-{log.created_at.date()}"
        if session_key not in sessions:
            sessions[session_key] = {
                "agent": log.agent,
                "date": str(log.created_at.date()),
                "logs": []
            }
        sessions[session_key]["logs"].append({
            "stage": log.stage,
            "message": log.message,
            "timestamp": str(log.created_at)
        })

    return {"sessions": list(sessions.values())}

@router.get("/session/{session_id}/logs")
async def get_session_logs(
    session_id: str,
    current_user: Profile = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get logs for a specific session"""
    # For now, return all user logs (in production, filter by session)
    logs = db.query(Log).filter(Log.user_id == current_user.id).order_by(Log.created_at.desc()).all()

    return {
        "session_id": session_id,
        "logs": [
            {
                "stage": log.stage,
                "message": log.message,
                "timestamp": str(log.created_at),
                "agent": log.agent
            }
            for log in logs
        ]
    }