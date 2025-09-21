# uvicorn writer_adapter:app --port 7002 --reload
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Any, Dict, AsyncGenerator
import json
import uuid

from MultiAgents_Workflow.agents.ReportAgent.graph.graph import build_writer_from_markdown_graph

writer_graph = build_writer_from_markdown_graph().compile()

router = APIRouter(tags=["Writer Agent Adapter"])

class InvokeIn(BaseModel):
    input: Dict[str, Any] = {}
    session_id: str | None = None

def _thread_cfg(session_id: str | None) -> Dict[str, Any]:
    tid = session_id or str(uuid.uuid4())
    return {"configurable": {"thread_id": tid}}

@router.post("/invoke")
def invoke(inp: InvokeIn):
    # expected input layout:
    # {
    #   "task": "...",
    #   "finalize_report": { "final_report": "<markdown>" },
    #   "analysis": {...}, "notes": {...}, "theme": {...}
    # }
    state = writer_graph.invoke(inp.input, _thread_cfg(inp.session_id))
    return JSONResponse({
        "ok": True,
        "output": {
            "html":    state.get("html"),
            "pdf_path":state.get("pdf_path"),
            "events":  state.get("events", []),
        }
    })

@router.get("/stream")
async def stream(request: Request, session_id: str | None = None,
                 task: str | None = None):
    async def gen() -> AsyncGenerator[bytes, None]:
        initial = {
            "task": task or "Generated Report",
            "events": [],
            # you can also accept ?md=... and inject into finalize_report
        }
        async for event in writer_graph.astream_events(initial, _thread_cfg(session_id)):
            payload = {
                "agent": "writer",
                "event": event.get("event"),
                "data":  event.get("data"),
                "tags":  event.get("tags"),
            }
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")
            if await request.is_disconnected():
                break
    return StreamingResponse(gen(), media_type="text/event-stream")
