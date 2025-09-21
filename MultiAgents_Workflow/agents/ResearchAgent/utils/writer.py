from MultiAgents_Workflow.agents.ResearchAgent.prompt.section_writer import section_writer_instructions
from MultiAgents_Workflow.agents.ResearchAgent.llm.llm import chat
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from MultiAgents_Workflow.agents.ResearchAgent.schemas.research_schema import ResearchState
import sys




def write_section(state:ResearchState):
    """
    Write a section of a report based on the source documents.
    """

    interview = state['interview']
    analyst = state['analyst']
    context = state['context']

    print(f"[write_section] Analyst: {analyst['name']}", file=sys.stderr)
    print(f"[write_section] Interview length: {len(interview) if interview else 0}", file=sys.stderr)
    print(f"[write_section] Context length: {len(str(context)) if context else 0}", file=sys.stderr)

    if not context or len(str(context)) == 0:
        print(f"[write_section] ERROR: No context available for writing section", file=sys.stderr)
        return {'sections': [f"ERROR: No context available for {analyst['name']}"]}

    system_message = section_writer_instructions.format(focus = analyst['persona'])
    print(f"[write_section] Sending to OpenAI...", file=sys.stderr)
    section = chat.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Use this source to write your section: {context}")])

    section_content = section.content if section else f"ERROR: No response from OpenAI for {analyst['name']}"
    print(f"[write_section] Generated section length: {len(section_content)}", file=sys.stderr)
    print(f"[write_section] Section preview: {section_content[:200]}...", file=sys.stderr)

    return {'sections': [section_content]}


