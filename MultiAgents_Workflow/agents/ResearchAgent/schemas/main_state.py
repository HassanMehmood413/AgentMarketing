from typing import TypedDict, List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
from typing import Annotated
import operator
from MultiAgents_Workflow.agents.ResearchAgent.schemas.analyst_schema import AnalystDict as Analyst    

class Interview(TypedDict):
    analyst: Analyst
    question: str
    answer: str
    context: List[str]


class Section(TypedDict):
    title: str
    content: str


class ResearchGraphState(TypedDict):
    topic:str
    max_analysts: int
    human_analyst_feedback: str
    analysts : list[Analyst]
    sections : Annotated[list,operator.add]
    introduction:str
    content:str
    conclusion:str
    final_report:str



