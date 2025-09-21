from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
from langgraph.types import Command, interrupt
from schemas.analyst_schema import GenerateAnalystState,Perspectives
from prompt.analyst_instructions import analyst_instructions
from llm.llm import chat
import sys



def create_analyst_personas(state: GenerateAnalystState):
    """Create analyst personas based on the research topic and feedback.
    
    Args:
        state (GenerateAnalystState): The state object containing the research topic and feedback.
        
    Returns:
        dict: Updated state with analyst personas.
    """
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    system_message = analyst_instructions.format(
        topic=topic,
        max_analysts=max_analysts,
        human_analyst_feedback=human_analyst_feedback
    )

    analysts = chat.invoke([SystemMessage(content=system_message)] + [HumanMessage(content="Generate the set of analysts")])
    parsed_analysts = PydanticOutputParser(pydantic_object=Perspectives).parse(analysts.content)

    return {"analysts": parsed_analysts.analysts}



def human_feedback(state: GenerateAnalystState):
    """Ask the user for feedback on the generated analyst personas.

    Args:
        state (GenerateAnalystState): The state object containing the generated analyst personas.

    Returns:
        dict or Command: The user's feedback on the generated analyst personas.
    """
    # Check if feedback is already provided (non-interactive mode)
    existing_feedback = state.get('human_analyst_feedback')
    if existing_feedback:
        print(f"[human_feedback] Using provided feedback: {existing_feedback}", file=sys.stderr)
        return {"human_analyst_feedback": existing_feedback}

    # Interactive mode - display current analysts for feedback
    analysts_display = "\n".join([analyst.persona for analyst in state.get('analysts', [])])
    feedback_prompt = f"""
          Please provide feedback on the generated analyst personas for topic: {state['topic']}

          Current Analysts:
          {analysts_display}

          Please provide your feedback (or type 'continue' to proceed):
    """

    print(f"[human_feedback] Interactive mode - prompting for feedback", file=sys.stderr)
    human_feedback_response = interrupt(feedback_prompt)
    return {"human_analyst_feedback": human_feedback_response}

def should_continue(state: GenerateAnalystState) -> Command[Literal['create_analysts', "__END__"]]:
    """Check if the user wants to continue with the research module.
    
    Args:
        state (GenerateAnalystState): The state object containing the user's feedback.
        
    Returns:
        Command: Direction to go to create_analysts or end.
    """
    human_feedback = state.get('human_analyst_feedback', '')
    
    if human_feedback and human_feedback.lower() != 'continue':
        return Command(goto="create_analysts")
    return Command(goto="__END__")