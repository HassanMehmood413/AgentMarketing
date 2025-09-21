from MultiAgents_Workflow.agents.ResearchAgent.schemas.research_schema import ResearchState
from MultiAgents_Workflow.agents.ResearchAgent.prompt.answer_instructions import answer_instructions
from MultiAgents_Workflow.agents.ResearchAgent.llm.llm import chat
from langchain_core.messages import SystemMessage
from langchain_core.messages import get_buffer_string
from langchain_core.messages import AIMessage
import sys



def generate_answer(state: ResearchState):
    """Generate an answer to the analyst's question."""

    analyst = state['analyst']
    messages = state['messages']
    context = state['context']

    system_message = answer_instructions.format(goals=analyst['persona'],context=context)
    answer = chat.invoke([SystemMessage(content=system_message)] + messages)

    answer.name = 'expert'

    return {'messages':[answer]}



def save_interview(state: ResearchState):
    """Save the interview to the database."""

    messages = state['messages']

    interview = get_buffer_string(messages)
    return {'interview': interview}



def route_messages(state: ResearchState,name: str = "expert"):
    """Route the messages to the appropriate function based on the message type."""

    messages = state['messages']
    max_num_turns = state.get("max_num_turns",2)

    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == name])

    print(f"[route_messages] num_responses: {num_responses}, max_num_turns: {max_num_turns}", file=sys.stderr)

    # End if expert has answered more than the max turns
    if num_responses >= max_num_turns:
        print(f"[route_messages] Ending interview - max turns reached", file=sys.stderr)
        return 'save_interview'

    # This router is run after each question - answer pair
    # Get the last question asked to check if it signals the end of discussion
    last_question = messages[-2]
    # Check if the text includes "Thank you so much for your help!" and in start we may have Alex: etc.

    if "thank you so much for your help!" in last_question.content.lower():
        return 'save_interview'
    return "ask_question"


