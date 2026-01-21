from pydantic import BaseModel, Field
from typing import List

class IssueAnalysis(BaseModel):
    summary: str = Field(..., description="One-sentence summary of the issue")
    type: str = Field(..., description="bug, feature_request, documentation, question, or other")
    priority_score: int = Field(..., ge=1, le=5, description="Score from 1 (low) to 5 (critical)")
    suggested_labels: List[str] = Field(..., min_items=2, max_items=3)
    potential_impact: str = Field(..., description="Impact if unresolved")
