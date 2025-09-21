from __future__ import annotations
from typing import TypedDict, Dict, Any, List, Optional
from markdown import markdown 






# -----------------------------
class WriterState(TypedDict):
    # INPUTS
    task: str
    events: List[Dict[str, Any]]
    finalize_report: Dict[str, Any]          # { "final_report": "<markdown>" }
    analysis: Dict[str, Any]                 # optional
    notes: Dict[str, Any]                    # optional
    # OPTIONS
    theme: Dict[str, Any]                    # e.g., {"show_toc": True, "show_references": True, "pdf_engine":"xhtml2pdf"}
    # INTERNAL
    sections: List[Dict[str, str]]           # [{"id","title","md","html"}]
    toc: List[Dict[str, str]]                # [{"id","title"}]
    sources: List[str]
    has_sources_section: bool
    # OUTPUTS
    html: Optional[str]
    pdf_path: Optional[str]