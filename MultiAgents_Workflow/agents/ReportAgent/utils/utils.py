from __future__ import annotations
from typing import TypedDict, Dict, Any, List, Optional
from langgraph.types import Command
from datetime import datetime
import os, re, uuid, html
from markdown import markdown as md_to_html
from bs4 import BeautifulSoup
from MultiAgents_Workflow.agents.ReportAgent.schemas.schema import WriterState
from jinja2 import Environment, BaseLoader, select_autoescape

XHTML_OK = False
HTML_ENGINE = None
try:
    from xhtml2pdf import pisa
    XHTML_OK = True
except Exception:
    XHTML_OK = False

# -----------------------------
# Utilities
# -----------------------------
def _emit(state: WriterState, stage: str, msg: str, extra: Dict[str, Any] | None = None):
    evt = {"stage": stage, "msg": msg}
    if extra: evt.update(extra)
    state["events"].append(evt)

def _now() -> str:
    return datetime.now().strftime("%b %d, %Y ΓÇó %I:%M %p")

_slug_re = re.compile(r"[^a-z0-9\-]+")
def _slug(s: str) -> str:
    s = (s or "section").strip().lower().replace(" ", "-")
    s = _slug_re.sub("", s)
    return s or ("s-" + uuid.uuid4().hex[:6])

_link_re = re.compile(r"\bhttps?://\S+")
def _extract_urls(md: str) -> List[str]:
    urls = _link_re.findall(md or "")
    seen, out = set(), []
    for u in urls:
        u = u.rstrip(")];,")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def _split_markdown(md: str) -> List[Dict[str, str]]:
    if not md or not md.strip():
        return [{"id": "intro", "title": "Report", "md": ""}]
    lines = md.splitlines()
    sections: List[Dict[str, str]] = []
    buf: List[str] = []
    current_title = None

    def flush():
        if current_title is None and not buf:
            return
        title = current_title or "Section"
        sec_md = "\n".join(buf).strip()
        sections.append({"id": _slug(title), "title": title.strip("# ").strip(), "md": sec_md})

    for ln in lines:
        if ln.startswith("## "):
            flush(); current_title = ln[3:].strip(); buf = []
        elif ln.startswith("# "):
            flush(); current_title = ln[2:].strip(); buf = []
        else:
            buf.append(ln)
    flush()
    if not sections:
        sections = [{"id": "report", "title": "Report", "md": md}]
    return sections

def _render_md_html(md_text: str) -> str:
    return md_to_html(
        md_text or "",
        extensions=["extra", "sane_lists", "smarty", "tables", "fenced_code"]
    )

def _stream_section_html(state: WriterState, sec: Dict[str, str]):
    """
    Convert a section's Markdown to HTML and emit 'writer_delta' chunks for real-time UI.
    IMPORTANT: Do NOT include the <h2> heading in sec["html"]; template renders it.
    """
    html_full = _render_md_html(sec["md"])
    soup = BeautifulSoup(html_full, "html.parser")

    heading = f"<h2 id='{sec['id']}'>{html.escape(sec['title'])}</h2>"
    _emit(state, "writer_delta", heading, {"section_id": sec["id"]})

    body_parts = []
    for el in soup.contents:
        frag = str(el).strip()
        if not frag:
            continue
        _emit(state, "writer_delta", frag, {"section_id": sec["id"]})
        body_parts.append(frag)

    return "".join(body_parts)

# -----------------------------
# Template (clean, print-ready)
# -----------------------------
REPORT_TMPL = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{{ title }}</title>
<style>
  :root { --ink:#0f172a; --muted:#475569; --brand:#2563eb; --bg:#ffffff; --card:#f8fafc; --border:#e2e8f0; }
  *{box-sizing:border-box} body{margin:0;font:14px/1.6 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg)}
  .wrap{padding:36px 40px 60px}
  .hero{border-radius:18px;padding:28px;background:
      radial-gradient(120% 140% at 90% 0%, rgba(37,99,235,.08), transparent 50%),
      radial-gradient(120% 120% at 0% 100%, rgba(14,165,233,.10), transparent 50%),
      linear-gradient(180deg,#fff,#f8fafc 70%);
      border:1px solid var(--border);box-shadow:0 10px 28px rgba(2,6,23,.08)}
  h1{margin:0 0 6px;font-size:28px;letter-spacing:.2px}
  .subtitle{color:var(--muted);font-weight:500;margin-bottom:4px}
  .kpis{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px}
  .kpi{background:#fff;border:1px solid var(--border);border-radius:14px;padding:12px 14px;min-width:140px;box-shadow:0 6px 16px rgba(2,6,23,.05)}
  .kpi b{font-size:18px;display:block}
  .card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;margin-top:14px}
  h2{font-size:18px;margin:0 0 10px}
  table{width:100%;border-collapse:collapse} th,td{border:1px solid var(--border);padding:8px 10px;text-align:left}
  th{background:#eef2ff}
  a{color:var(--brand);text-decoration:none}
  .toc a{color:var(--muted)}
  .footer{color:#94a3b8;font-size:12px;text-align:center;margin-top:26px}
</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>{{ title }}</h1>
      <div class="subtitle">{{ subtitle }}</div>
      <div class="kpis">
        <div class="kpi"><span>Sections</span><b>{{ sections|length }}</b></div>
        <div class="kpi"><span>Sources</span><b>{{ sources|length }}</b></div>
      </div>
    </div>

    {% if show_toc and toc and toc|length>1 %}
    <div class="card toc">
      <h2>Table of Contents</h2>
      <ol>
        {% for t in toc %}
          <li><a href="#{{ t.id }}">{{ t.title }}</a></li>
        {% endfor %}
      </ol>
    </div>
    {% endif %}

    {% for s in sections %}
      <div class="card">
        <h2 id="{{ s.id }}">{{ s.title }}</h2>
        <div>{{ s.html | safe }}</div>
      </div>
    {% endfor %}

    {% if pricing_table and pricing_table|length>0 %}
    <div class="card">
      <h2>Pricing / Comparison</h2>
      <table>
        <thead><tr><th>Item</th><th>Your Price</th><th>Competitor</th></tr></thead>
        <tbody>
        {% for row in pricing_table %}
          <tr>
            <td>{{ row.get('name','') }}</td>
            <td>{{ row.get('you','') }}</td>
            <td>{{ row.get('competitor','') }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
    {% endif %}

    {% if show_refs and sources and sources|length>0 %}
    <div class="card">
      <h2>References</h2>
      <ol>
        {% for u in sources %}
          <li><a href="{{ u }}">{{ u }}</a></li>
        {% endfor %}
      </ol>
    </div>
    {% endif %}

    <div class="footer">Generated by Writer Agent ΓÇó {{ subtitle }}</div>
  </div>
</body>
</html>
"""

_env = Environment(loader=BaseLoader(), autoescape=select_autoescape(enabled_extensions=("html","xml")))
_template = _env.from_string(REPORT_TMPL)

# -----------------------------
# Nodes
# -----------------------------
def ingest_markdown(state: WriterState) -> WriterState:
    try:
        raw_md = ""
        if "finalize_report" in state and isinstance(state["finalize_report"], dict):
            raw_md = state["finalize_report"].get("final_report", "") or ""
        elif "final_report" in state:
            raw_md = state["final_report"] or ""
        if not raw_md:
            raw_md = "# Report\n\n_No content provided by research agent._"

        secs = _split_markdown(raw_md)
        for s in secs:
            s["html"] = ""

        state["sections"] = secs
        state["toc"] = [{"id": s["id"], "title": s["title"]} for s in secs]
        state["has_sources_section"] = any(s["title"].strip().lower() == "sources" for s in secs)

        # sources
        urls = _extract_urls(raw_md)
        sources = []
        for u in (state.get("analysis", {}).get("citations") or []):
            if isinstance(u, str): sources.append(u)
            elif isinstance(u, dict) and u.get("url"): sources.append(u["url"])
        if not sources:
            for u in (state.get("notes", {}).get("sources") or []):
                if isinstance(u, str): sources.append(u)
                elif isinstance(u, dict) and u.get("url"): sources.append(u["url"])
        if not sources:
            sources = urls
        state["sources"] = list(dict.fromkeys(sources))

        _emit(state, "writer", f"Ingested markdown ({len(secs)} sections)")
    except Exception as e:
        _emit(state, "writer_error", f"ingest_markdown failed: {e}")
        state["sections"] = [{"id": "report", "title": "Report", "md": ""}]
        state["toc"] = [{"id": "report", "title": "Report"}]
        state["sources"] = []
        state["has_sources_section"] = False
    return state

def stream_sections(state: WriterState) -> WriterState:
    try:
        for sec in state["sections"]:
            _emit(state, "writer", f"Rendering '{sec['title']}'", {"section_id": sec["id"]})
            sec_html = _stream_section_html(state, sec)
            sec["html"] = sec_html
            _emit(state, "writer", f"Completed '{sec['title']}'", {"section_id": sec["id"]})
    except Exception as e:
        _emit(state, "writer_error", f"stream_sections failed: {e}")
    return state

def compile_html(state: WriterState) -> WriterState:
    try:
        show_toc = bool(state.get("theme", {}).get("show_toc", True))
        theme_show_refs = state.get("theme", {}).get("show_references", True)
        has_sources_section = bool(state.get("has_sources_section", False))
        show_refs = bool(theme_show_refs) and not has_sources_section
        pricing_table = state.get("analysis", {}).get("pricing_table") or []

        html_out = _template.render(
            title=f"Report: {state.get('task','Analysis')}",
            subtitle=_now(),
            sections=state.get("sections", []),
            toc=state.get("toc", []),
            sources=state.get("sources", []),
            show_toc=show_toc,
            pricing_table=pricing_table,
            show_refs=show_refs,
        )
        state["html"] = html_out or "<html><body><p>Empty report.</p></body></html>"
        _emit(state, "writer", "Compiled HTML")
    except Exception as e:
        _emit(state, "writer_error", f"compile_html failed: {e}")
        state["html"] = "<html><body><p>Compilation error.</p></body></html>"
    return state

def _select_pdf_engine(state: WriterState) -> str:
    override = (state.get("theme", {}) or {}).get("pdf_engine")
    if override in {"xhtml2pdf", "none"}:
        return override
    # auto
    if XHTML_OK:
        return "xhtml2pdf"
    return "none"

def export_pdf(state: WriterState) -> WriterState:
    try:
        os.makedirs("reports", exist_ok=True)
        base_name = f"{state.get('task','Report').replace(' ','_')[:60]}"
        out_pdf = f"reports/{base_name}.pdf"
        engine = _select_pdf_engine(state)



        if engine == "xhtml2pdf" and XHTML_OK and pisa is not None:
            try:
                with open(out_pdf, "wb") as f:
                    # xhtml2pdf expects a file-like object
                    result = pisa.CreatePDF(state.get("html") or "<html></html>", dest=f)
                if not result.err and os.path.exists(out_pdf):
                    state["pdf_path"] = out_pdf
                    _emit(state, "writer", "PDF ready (xhtml2pdf)", {"path": out_pdf})
                    return state
                else:
                    _emit(state, "writer_error", "xhtml2pdf failed; writing HTML instead.")
            except Exception as e:
                _emit(state, "writer_error", f"xhtml2pdf failed: {e}")

        # Fallback: save HTML next to intended PDF
        out_html = f"reports/{base_name}.html"
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(state.get("html") or "<html></html>")
        state["pdf_path"] = out_html
        _emit(state, "writer", "Saved HTML (PDF engine unavailable)", {"path": out_html})
    except Exception as e:
        _emit(state, "writer_error", f"export_pdf failed: {e}")
        state["pdf_path"] = None
    return state

def done_or_stream(state: WriterState) -> str:
    if not state.get("sections"):
        return "compile_html"
    return "stream_sections"

