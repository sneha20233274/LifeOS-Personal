# backend/app/schemas/goal.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class GoalCreate(BaseModel):
    goal_name: str = Field(..., max_length=200)
    description: Optional[str] = None

    # matches model
    target_date: Optional[date] = None

    # user-controlled metadata
    importance_level: int = Field(default=1, ge=1, le=5)
    motivations: Optional[List[str]] = None


class GoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    importance_level: Optional[int] = Field(None, ge=1, le=5)
    motivations: Optional[List[str]] = None   # ✅ added


class GoalOut(BaseModel):
    goal_id: int
    user_id: int

    goal_name: str
    description: Optional[str]

    target_date: Optional[date]
    importance_level: int
    motivations: Optional[List[str]] = None   # ✅ added

    percent_completion: float
    created_at: datetime

    class Config:
        orm_mode = True
