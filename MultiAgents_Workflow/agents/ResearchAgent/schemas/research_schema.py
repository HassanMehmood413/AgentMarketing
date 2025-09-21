from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage
import operator 
from typing import Annotated
from pydantic import BaseModel,Field
from langgraph.graph import MessagesState
from MultiAgents_Workflow.agents.ResearchAgent.schemas.analyst_schema import AnalystDict as Analyst

class Interview(BaseMessage):
    analyst: Analyst
    question: str
    answer: str
    context: List[str]


class ResearchState(MessagesState):
    max_num_turns:int
    context: Annotated[list,operator.add]
    analyst: Analyst
    interview:str
    sections: list

class SearchQuery(BaseModel):
    search_query: str = Field(None,description="Search query for retrieval")


