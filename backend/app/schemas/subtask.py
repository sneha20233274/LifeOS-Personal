
# backend/app/schemas/subtask.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class SubtaskCreate(BaseModel):
    subtask_name: str
    subtask_description: Optional[str] = None
    difficulty_rating: Optional[int] = 1
    deadline: Optional[date] = None
    task_id: int
    goal_id: int

class SubtaskUpdate(BaseModel):
    subtask_name: Optional[str]
    subtask_description: Optional[str]
    difficulty_rating: Optional[int]
    achieved: Optional[bool]
    deadline: Optional[date]

class SubtaskOut(BaseModel):
    subtask_id: int
    task_id: int
    goal_id: int
    user_id: int
    subtask_name: Optional[str]
    achieved: bool
    created_at: datetime

    class Config:
        orm_mode = True
