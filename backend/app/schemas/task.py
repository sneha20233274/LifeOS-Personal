# backend/app/schemas/task.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TaskCreate(BaseModel):
    task_name: str
    task_description: Optional[str] = None
    task_deadline: Optional[date] = None
    difficulty_level: Optional[int] = 1
    goal_id: int

class TaskUpdate(BaseModel):
    task_name: Optional[str]
    task_description: Optional[str]
    task_deadline: Optional[date]
    difficulty_level: Optional[int]
    percent_completion: Optional[float]

class TaskOut(BaseModel):
    task_id: int
    goal_id: int
    user_id: int
    task_name: str
    percent_completion: float
    created_at: datetime

    class Config:
        orm_mode = True
