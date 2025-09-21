from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Any, Dict, AsyncGenerator
import json, uuid

from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Log

# Import the research graph (with proper path handling)
import sys
from pathlib import Path

agent_dir = Path(__file__).parent.parent.parent / "agents" / "ResearchAgent" / "graph"
sys.path.insert(0, str(agent_dir.parent.parent))

try:
    from agents.ResearchAgent.graph.graph_main import graph as research_graph
except ImportError:
    # Fallback for different environments
    from ...agents.ResearchAgent.graph.graph_main import graph as research_graph

router = APIRouter(tags=["Research Agent Adapter"])

class InvokeIn(BaseModel):
    input: Dict[str, Any] = {}
    session_id: str | None = None
    user_id: int | None = None  # optional, to attach logs to a user

def _thread_cfg(session_id: str | None) -> Dict[str, Any]:
    return {"configurable": {"thread_id": session_id or str(uuid.uuid4())}}

def save_log(db: Session, user_id: int | None, agent: str, stage: str, message: str):
    if user_id is None:
        return
    db.add(Log(user_id=user_id, agent=agent, stage=stage, message=message))
    db.commit()

@router.post("/invoke")
async def invoke(inp: InvokeIn, db: Session = Depends(get_db)):
    payload = dict(inp.input or {})
    payload.setdefault("human_analyst_feedback", "continue")

    state = await research_graph.ainvoke(payload, _thread_cfg(inp.session_id))

    # persist any internal events if present
    for evt in state.get("events", []):
        save_log(db, inp.user_id, "research", evt.get("stage","event"), json.dumps(evt))

    return JSONResponse({
        "ok": True,
        "output": {
            "finalize_report": state.get("finalize_report", {}),
            "write_report":    state.get("write_report", {}),
            "write_intro":     state.get("write_introduction", {}),
            "write_conclusion":state.get("write_conclusion", {}),
            "events":          state.get("events", []),
        }
    })

@router.get("/stream")
async def stream(request: Request, db: Session = Depends(get_db),
                 session_id: str | None = None, topic: str | None = None,
                 max_analysts: int = 5, user_id: int | None = None):
    async def gen() -> AsyncGenerator[bytes, None]:
        initial = {
            "topic": topic or "Competitive analysis",
            "max_analysts": max_analysts,
            "human_analyst_feedback": "continue",
        }
        async for event in research_graph.astream_events(initial, _thread_cfg(session_id)):
            payload = {
                "agent": "research",
                "event": event.get("event"),
                "data":  event.get("data"),
                "tags":  event.get("tags"),
            }
            save_log(db, user_id, "research", payload["event"] or "event", json.dumps(payload))
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")
            if await request.is_disconnected():
                break
    return StreamingResponse(gen(), media_type="text/event-stream")