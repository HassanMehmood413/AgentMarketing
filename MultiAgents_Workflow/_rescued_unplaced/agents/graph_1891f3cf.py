# agents/ReportAgent/mcp_entry.py
from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path
import os

agent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(agent_dir))

from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableLambda

# Your existing writer state + node funcs - using absolute imports
from schemas.schema import WriterState
from utils.utils import (
    ingest_markdown,
    stream_sections,
    compile_html,
    export_pdf,
    done_or_stream,
)

# Γ£à FastMCP provides the @tool decorator
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server


# -----------------------------
# Build the Writer graph once
# -----------------------------
def build_writer_from_markdown_graph() -> StateGraph:
    g = StateGraph(WriterState)
    g.add_node("ingest_markdown", RunnableLambda(ingest_markdown))
    g.add_node("stream_sections", RunnableLambda(stream_sections))
    g.add_node("compile_html", RunnableLambda(compile_html))
    g.add_node("export_pdf", RunnableLambda(export_pdf))

    g.add_edge(START, "ingest_markdown")
    g.add_conditional_edges("ingest_markdown", done_or_stream, ["stream_sections", "compile_html"])
    g.add_edge("stream_sections", "compile_html")
    g.add_edge("compile_html", "export_pdf")
    g.add_edge("export_pdf", END)
    return g

# Compile once at import time
WRITER_GRAPH = build_writer_from_markdown_graph().compile()


# -----------------------------
# MCP server
# -----------------------------
mcp = FastMCP("report-agent")


@mcp.tool()
async def generate_report(
    task: str = "Generate comprehensive report"
) -> dict:
    """
    Generate a professional report from research results.
    Gets research data from Research Agent and creates formatted output.
    Returns: { html, pdf_path, events }
    """
    # Try to get research results from Research Agent via MCP
    research_data = {"final_report": "# Research Report\n\n_No research data available._"}

    # Check if we're running under Coral orchestration
    coral_runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME")
    if coral_runtime:
        print("Attempting to get research results from shared file...", file=sys.stderr)
        try:
            # Try to read research results from shared file
            shared_file = Path(__file__).parent.parent.parent / "shared_research_results.json"
            if shared_file.exists():
                import json
                with open(shared_file, 'r', encoding='utf-8') as f:
                    research_data = json.load(f)
                print(f"Successfully loaded research results from shared file", file=sys.stderr)
                print(f"Research report length: {len(research_data.get('final_report', ''))}", file=sys.stderr)
                print(f"Number of sections: {len(research_data.get('sections', []))}", file=sys.stderr)
            else:
                print(f"Shared research file not found: {shared_file}", file=sys.stderr)
                # Fallback: try to read from environment variable
                research_content = os.getenv("RESEARCH_REPORT_CONTENT")
                if research_content:
                    research_data = {"final_report": research_content}
                    print("Retrieved research content from environment variable", file=sys.stderr)
                else:
                    print("No research content available from any source", file=sys.stderr)
                    research_data = {"final_report": "# Research Report\n\n_No research data found._"}

        except Exception as e:
            print(f"Error retrieving research results: {e}", file=sys.stderr)
            research_data = {"final_report": f"# Research Report\n\n_Error loading research data: {e}_"}
    else:
        print("Not running under Coral orchestration - using dummy data", file=sys.stderr)
        research_data = {"final_report": "# Research Report\n\n_Standalone mode - no research data available._"}

    # Initial state for the writer agent
    final_report_content = research_data.get("final_report", "# Report\n\n_No content provided._")

    state: WriterState = {
        "task": task,
        "events": [],
        "finalize_report": {"final_report": final_report_content},
        "analysis": research_data.get("analysts", []),
        "notes": research_data.get("events", []),
        "theme": {"show_toc": True},
        "sections": research_data.get("sections", []),
        "toc": [],
        "sources": [],
        "html": None,
        "pdf_path": None,
    }

    # Γ£à Use async invoke (donΓÇÖt try to for-loop astream() without async)
    final_state = await WRITER_GRAPH.ainvoke(state)

    return {
        "html": final_state.get("html", ""),
        "pdf_path": final_state.get("pdf_path"),
        "events": final_state.get("events", []),  # surface streaming logs to UI
    }


@mcp.tool()
async def get_report_status() -> str:
    """Quick health/status check for the writer agent."""
    return "Report agent is ready."


async def main():
    # Check if we're running under Coral orchestration
    coral_runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME")

    if coral_runtime:
        # When running under Coral, generate report immediately
        print("Running under Coral orchestration - generating report", file=sys.stderr)

        try:
            # Generate the report
            result = await generate_report()
            print(f"Report Agent completed successfully. HTML length: {len(result.get('html', ''))}", file=sys.stderr)
            print(f"PDF path: {result.get('pdf_path', 'None')}", file=sys.stderr)

            # Keep the process alive briefly so Coral can capture the result
            await asyncio.sleep(5)

        except Exception as e:
            print(f"Report Agent failed: {e}", file=sys.stderr)
            import traceback
            print(f"Traceback: {traceback.format_exc()}", file=sys.stderr)
    else:
        # Standalone MCP mode - use stdio
        print("Running in standalone MCP mode", file=sys.stderr)
        async with stdio_server() as (read, write):
            await mcp.run(read, write)


if __name__ == "__main__":
    asyncio.run(main())