from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage
from MultiAgents_Workflow.agents.ResearchAgent.schemas.main_state import ResearchGraphState
from MultiAgents_Workflow.agents.ResearchAgent.graph.analyst_graph import create_analyst_personas
from MultiAgents_Workflow.agents.ResearchAgent.utils.personas import human_feedback
from MultiAgents_Workflow.agents.ResearchAgent.graph.serach_ask_answer import conduct_all_interviews_node
from MultiAgents_Workflow.agents.ResearchAgent.utils.main_util import initialize_all_interview_states
from MultiAgents_Workflow.agents.ResearchAgent.utils.main_util import write_report
from MultiAgents_Workflow.agents.ResearchAgent.utils.main_util import write_introduction
from MultiAgents_Workflow.agents.ResearchAgent.utils.main_util import write_conclusion
from MultiAgents_Workflow.agents.ResearchAgent.utils.main_util import finalize_report
from MultiAgents_Workflow.agents.ResearchAgent.schemas.main_state import ResearchGraphState

from dotenv import load_dotenv
import os,sys

import importlib
def _search_prompts():
    return importlib.import_module("MultiAgents_Workflow.agents.ResearchAgent.prompt.search_instructions")


load_dotenv()




# Add nodes and edges
builder: StateGraph = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analyst_personas)
# builder.add_node("human_feedback", human_feedback)
builder.add_node("initialize_interviews", initialize_all_interview_states)
builder.add_node("conduct_interview", conduct_all_interviews_node)
builder.add_node("write_report",write_report)
builder.add_node("write_introduction",write_introduction)
builder.add_node("write_conclusion",write_conclusion)
builder.add_node("finalize_report",finalize_report)

# def should_continue_main(state: ResearchGraphState) -> str:
#     """Determine if we should continue with interviews or go back to analyst creation."""
#     human_feedback = state.get('human_analyst_feedback', '')
#     if human_feedback and human_feedback.lower() != 'continue':
#         return "create_analysts"
#     return "initialize_interviews"

# Logic
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "initialize_interviews")
builder.add_edge("initialize_interviews", "conduct_interview")
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge(["write_conclusion", "write_report", "write_introduction"], "finalize_report")
builder.add_edge("finalize_report", END)

# Compile
memory: MemorySaver = MemorySaver()
graph: CompiledStateGraph = builder.compile(checkpointer=memory)
