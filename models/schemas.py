from pydantic import BaseModel
from typing import Optional, List


class QueryRequest(BaseModel):
    query: str


class ClauseReference(BaseModel):
    file: str
    clause: str


class DecisionResponse(BaseModel):
    decision: str
    amount: Optional[float]
    justification: str
    clauses_used: List[ClauseReference]
