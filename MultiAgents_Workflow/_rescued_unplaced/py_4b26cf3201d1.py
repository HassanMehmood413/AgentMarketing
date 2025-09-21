from schemas.main_state import ResearchGraphState
from langgraph.constants import Send
from langchain_core.messages import HumanMessage
from prompt.report_writer import report_writer_instructions
from llm.llm import chat
from langchain_core.messages import SystemMessage
from prompt.intro_conclusion import intro_conclusion_instructions
import sys


def initialize_all_interview_states(state:ResearchGraphState):
    """ This prepares the state for running interviews with all analysts """

    topic = state["topic"]
    max_analysts = state.get("max_analysts", 2)

    print(f"[initialize_all_interview_states] Setting up interviews for {len(state['analysts'])} analysts", file=sys.stderr)

    # Return state that sets up the interview subgraph to run for all analysts
    return {
        "analysts": state["analysts"],  # Pass analysts to interview subgraph
        "interviews": [],  # Will be populated
        "sections": []  # Will be populated by write_section
    }


def write_report(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    print(f"[write_report] Topic: {topic}", file=sys.stderr)
    print(f"[write_report] Number of sections: {len(sections) if sections else 0}", file=sys.stderr)

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    if not sections or len(sections) == 0:
        print(f"[write_report] ERROR: No sections to write report from!", file=sys.stderr)
        return {"content": "ERROR: No sections available to generate report"}

    print(f"[write_report] Sections preview: {formatted_str_sections[:200]}...", file=sys.stderr)

    # Summarize the sections into a final report
    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)
    print(f"[write_report] Sending to OpenAI...", file=sys.stderr)
    report = chat.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Write a report based upon these memos.")])

    content = report.content if report else "ERROR: No response from OpenAI"
    print(f"[write_report] Generated content length: {len(content)}", file=sys.stderr)
    print(f"[write_report] Content preview: {content[:200]}...", file=sys.stderr)

    return {"content": content}

def write_introduction(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    print(f"[write_introduction] Topic: {topic}", file=sys.stderr)
    print(f"[write_introduction] Number of sections: {len(sections) if sections else 0}", file=sys.stderr)

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    if not sections or len(sections) == 0:
        print(f"[write_introduction] ERROR: No sections to write introduction from!", file=sys.stderr)
        return {"introduction": "ERROR: No sections available to generate introduction"}

    print(f"[write_introduction] Sending to OpenAI...", file=sys.stderr)
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = chat.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")])

    introduction = intro.content if intro else "ERROR: No response from OpenAI"
    print(f"[write_introduction] Generated introduction length: {len(introduction)}", file=sys.stderr)
    print(f"[write_introduction] Introduction preview: {introduction[:200]}...", file=sys.stderr)

    return {"introduction": introduction}

def write_conclusion(state: ResearchGraphState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    print(f"[write_conclusion] Topic: {topic}", file=sys.stderr)
    print(f"[write_conclusion] Number of sections: {len(sections) if sections else 0}", file=sys.stderr)

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    if not sections or len(sections) == 0:
        print(f"[write_conclusion] ERROR: No sections to write conclusion from!", file=sys.stderr)
        return {"conclusion": "ERROR: No sections available to generate conclusion"}

    print(f"[write_conclusion] Sending to OpenAI...", file=sys.stderr)
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    conclusion = chat.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")])

    conclusion_text = conclusion.content if conclusion else "ERROR: No response from OpenAI"
    print(f"[write_conclusion] Generated conclusion length: {len(conclusion_text)}", file=sys.stderr)
    print(f"[write_conclusion] Conclusion preview: {conclusion_text[:200]}...", file=sys.stderr)

    return {"conclusion": conclusion_text}

def finalize_report(state: ResearchGraphState):
    """ The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """

    print(f"[finalize_report] State keys: {list(state.keys())}", file=sys.stderr)

    # Check if required fields exist
    required_fields = ["content", "introduction", "conclusion"]
    for field in required_fields:
        if field not in state:
            print(f"[finalize_report] ERROR: Missing required field '{field}'", file=sys.stderr)
            return {"final_report": f"ERROR: Missing required field '{field}'"}

    # Save full final report
    content = state["content"]
    introduction = state["introduction"]
    conclusion = state["conclusion"]

    print(f"[finalize_report] Content length: {len(content)}", file=sys.stderr)
    print(f"[finalize_report] Introduction length: {len(introduction)}", file=sys.stderr)
    print(f"[finalize_report] Conclusion length: {len(conclusion)}", file=sys.stderr)

    # Check for errors in content
    if content.startswith("ERROR:"):
        print(f"[finalize_report] Content has error: {content}", file=sys.stderr)
        return {"final_report": content}

    if introduction.startswith("ERROR:"):
        print(f"[finalize_report] Introduction has error: {introduction}", file=sys.stderr)
        return {"final_report": introduction}

    if conclusion.startswith("ERROR:"):
        print(f"[finalize_report] Conclusion has error: {conclusion}", file=sys.stderr)
        return {"final_report": conclusion}

    # Process content
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = introduction + "\n\n---\n\n" + content + "\n\n---\n\n" + conclusion
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources

    print(f"[finalize_report] Final report length: {len(final_report)}", file=sys.stderr)
    print(f"[finalize_report] Final report preview: {final_report[:300]}...", file=sys.stderr)

    return {"final_report": final_report}
