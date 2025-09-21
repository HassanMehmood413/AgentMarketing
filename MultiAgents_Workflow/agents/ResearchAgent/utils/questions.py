from MultiAgents_Workflow.agents.ResearchAgent.schemas.research_schema import ResearchState
from MultiAgents_Workflow.agents.ResearchAgent.prompt.question_instructions import FULL_PROMPT
from MultiAgents_Workflow.agents.ResearchAgent.llm.llm import chat
from langchain_core.messages import SystemMessage




def generate_questions(state: ResearchState):
    """ Node to generate a question """

    # Get state
    analyst = state["analyst"]
    messages = state["messages"]

    # Generate question
    system_message = FULL_PROMPT.format(goals=analyst['persona'])
    question = chat.invoke([SystemMessage(content=system_message)]+messages)

    # Write messages to state
    return {"messages": [question]}