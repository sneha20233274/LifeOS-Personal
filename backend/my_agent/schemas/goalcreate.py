from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
class GoalCreate(BaseModel):
    goal_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    start_date : date = Field(default_factory=date.today)
    target_date: Optional[date] = None

    importance_level: int = Field(default=1, ge=1, le=5)
    motivations: Optional[List[str]] = None