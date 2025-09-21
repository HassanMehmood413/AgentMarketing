from typing import List, Optional
from pydantic import BaseModel, Field
from typing import TypedDict


class Analyst(BaseModel):
    name: str = Field(description="Analyst Name")
    role: str = Field(description="Analyst Role")
    affiliation: str = Field(description="Primary Affiliation of the analyst")
    description: str = Field(description="Analyst Description")

    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"

class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(description="List of Analysts")

# TypedDict versions for LangGraph state
class AnalystDict(TypedDict):
    name: str
    persona: str

class GenerateAnalystState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str
    analysts: List[AnalystDict]

