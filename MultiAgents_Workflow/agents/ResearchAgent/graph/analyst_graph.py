from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from MultiAgents_Workflow.agents.ResearchAgent.schemas.analyst_schema import GenerateAnalystState
from MultiAgents_Workflow.agents.ResearchAgent.utils.personas import create_analyst_personas, human_feedback, should_continue



builder = StateGraph(GenerateAnalystState)

builder.add_node("create_analysts", create_analyst_personas)
builder.add_node("human_feedback", human_feedback)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue, ["create_analysts", END])

# Compile
memory: MemorySaver = MemorySaver()
graph: CompiledStateGraph = builder.compile(interrupt_before=['human_feedback'], checkpointer=memory)
