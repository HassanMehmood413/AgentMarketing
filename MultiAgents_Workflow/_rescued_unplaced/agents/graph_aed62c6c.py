# agents/ResearchAgent/mcp_entry.py
import os, sys
from pathlib import Path

# Add parent directory to path for relative imports when run as script
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph

# your existing imports - using absolute imports
import sys
from pathlib import Path

# Add the agent directory to path so we can import
agent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(agent_dir))

from schemas.main_state import ResearchGraphState
from utils.main_util import (
    initialize_all_interview_states, write_report,
    write_introduction, write_conclusion, finalize_report
)
from utils.personas import create_analyst_personas, human_feedback
from graph.serach_ask_answer import conduct_all_interviews_node

# Γ£à use FastMCP (has the @tool decorator)
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.stdio import stdio_server

# ---------- build your research graph (unchanged) ----------
builder: StateGraph = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analyst_personas)
# builder.add_node("human_feedback", human_feedback)
builder.add_node("initialize_interviews", initialize_all_interview_states)
builder.add_node("conduct_interview", conduct_all_interviews_node)
builder.add_node("write_report", write_report)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "initialize_interviews")
builder.add_edge("initialize_interviews", "conduct_interview")
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge(["write_conclusion", "write_report", "write_introduction"], "finalize_report")
builder.add_edge("finalize_report", END)

memory = MemorySaver()
graph: CompiledStateGraph = builder.compile(
    checkpointer=memory
)

# ---------- MCP server ----------
mcp = FastMCP("research-agent")

# Global storage for research results (for inter-agent communication)
research_results = {}

@mcp.tool()
async def conduct_research(topic: str = "Nike pricing strategy", max_analysts: int = 2) -> dict:
    """
    Conduct comprehensive research on a topic using multiple analyst perspectives.
    Returns a dict with final_report and useful extras.
    """
    initial_state = {
        "messages": [],
        "analysts": [],
        "interviews": {},
        "sections": [],
        "introduction": "",
        "conclusion": "",
        "final_report": "",
        "topic": topic,
        "max_analysts": max_analysts
    }
    config = {"configurable": {"thread_id": f"research-{topic.replace(' ', '-')[:40]}" }}
    result = await graph.ainvoke(initial_state, config)

    final_report = result.get("finalize_report", {}).get("final_report") or result.get("final_report", "")

    # Store results globally for other agents to access
    research_results[topic] = {
        "final_report": final_report,
        "analysts": [a.dict() if hasattr(a, "dict") else a for a in result.get("analysts", [])],
        "events": result.get("events", []),
        "sections": result.get("sections", []),
        "introduction": result.get("introduction", ""),
        "conclusion": result.get("conclusion", ""),
    }

    # Also save to a shared file for inter-agent communication
    import json
    shared_file = Path(__file__).parent.parent.parent / "shared_research_results.json"
    try:
        with open(shared_file, 'w', encoding='utf-8') as f:
            json.dump(research_results[topic], f, ensure_ascii=False, indent=2)
        print(f"Saved research results to shared file: {shared_file}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to save research results to file: {e}", file=sys.stderr)

    return research_results[topic]

@mcp.tool()
async def get_research_results(topic: str = None) -> dict:
    """
    Get the latest research results. If topic is provided, get results for that specific topic.
    Returns the research report and analysis.
    """
    if topic and topic in research_results:
        return research_results[topic]
    elif research_results:
        # Return the most recent results
        latest_topic = list(research_results.keys())[-1]
        return research_results[latest_topic]
    else:
        return {"error": "No research results available. Please run conduct_research first."}

@mcp.tool()
async def get_research_status() -> str:
    """Quick health/status for this agent."""
    return "Research agent is ready."

async def main(topic=None, max_analysts=None):
    # Check if we're running under Coral orchestration
    coral_runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME")

    if coral_runtime:
        # When running under Coral, run the research workflow
        print("Running under Coral orchestration", file=sys.stderr)

        # Use provided parameters or fall back to defaults
        if topic is None:
            topic = "Nike pricing strategy analysis"  # Default topic

        if max_analysts is None:
            max_analysts = 2  # Default number of analysts
        else:
            # Ensure it's an integer
            try:
                max_analysts = int(max_analysts)
            except (ValueError, TypeError):
                max_analysts = 2  # fallback to default

        # Also check for OpenAI key
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key

        print(f"Starting research on: {topic}", file=sys.stderr)

        # Run the research workflow
        initial_state = {
            "messages": [],
            "analysts": [],
            "interviews": {},
            "sections": [],
            "introduction": "",
            "conclusion": "",
            "final_report": "",
            "topic": topic,
            "max_analysts": max_analysts
        }

        config = {"configurable": {"thread_id": f"research-{topic.replace(' ', '-')[:40]}" }}

        try:
            print(f"Starting research workflow with initial state keys: {list(initial_state.keys())}", file=sys.stderr)

            result = await graph.ainvoke(initial_state, config)

            print(f"Research workflow completed. Result keys: {list(result.keys()) if result else 'None'}", file=sys.stderr)

            # Debug: Check key fields
            print(f"[DEBUG] analysts: {len(result.get('analysts', []))} items", file=sys.stderr)
            print(f"[DEBUG] sections: {len(result.get('sections', []))} items", file=sys.stderr)
            print(f"[DEBUG] introduction: {len(result.get('introduction', ''))} chars", file=sys.stderr)
            print(f"[DEBUG] conclusion: {len(result.get('conclusion', ''))} chars", file=sys.stderr)
            print(f"[DEBUG] content: {len(result.get('content', ''))} chars", file=sys.stderr)

            # Check for different possible result structures
            final_report = ""
            if "finalize_report" in result and result["finalize_report"]:
                if "final_report" in result["finalize_report"]:
                    final_report = result["finalize_report"]["final_report"]
                    print(f"Found final_report in finalize_report node: {len(final_report)} chars", file=sys.stderr)
                else:
                    print(f"finalize_report node exists but no final_report field", file=sys.stderr)
            elif "final_report" in result:
                final_report = result["final_report"]
                print(f"Found final_report in root result: {len(final_report)} chars", file=sys.stderr)
            else:
                print(f"No final_report found in result. Available keys: {list(result.keys()) if result else 'None'}", file=sys.stderr)

            print(f"Research completed. Final report length: {len(final_report)}", file=sys.stderr)

            # Debug: print some content if available
            if final_report and len(final_report) > 0:
                preview = final_report[:200] + "..." if len(final_report) > 200 else final_report
                print(f"Report preview: {preview}", file=sys.stderr)
            else:
                print("No report content generated", file=sys.stderr)

            # Keep the process alive briefly so Coral can capture the result
            await asyncio.sleep(2)
        except Exception as e:
            import traceback
            print(f"Research failed.: {e}", file=sys.stderr)
            print(f"Traceback: {traceback.format_exc()}", file=sys.stderr)

    else:
        # Standalone MCP mode - use stdio
        print("Running in standalone MCP mode", file=sys.stderr)
        async with stdio_server() as (read, write):
            await mcp.run(read, write)

if __name__ == "__main__":
    asyncio.run(main())