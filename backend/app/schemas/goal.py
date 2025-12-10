# backend/app/schemas/goal.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class GoalCreate(BaseModel):
    goal_name: str
    description: Optional[str] = None
    deadline: Optional[date] = None
    importance_level: Optional[int] = 1
    motivations: Optional[List[str]] = []

class GoalUpdate(BaseModel):
    goal_name: Optional[str]
    description: Optional[str]
    deadline: Optional[date]
    importance_level: Optional[int]
    percent_completion: Optional[float]

class GoalOut(BaseModel):
    goal_id: int
    user_id: int
    goal_name: str
    description: Optional[str]
    deadline: Optional[date]
    importance_level: int
    percent_completion: float
    created_at: datetime

    class Config:
        orm_mode = True
