from pydantic import BaseModel
from typing import List

class AgentRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    response: str
    sources: List[str]