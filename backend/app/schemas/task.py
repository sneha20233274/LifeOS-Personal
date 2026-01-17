# backend/app/schemas/task.py

from typing import Optional
from pydantic import BaseModel


class TaskCreate(BaseModel):
    task_name: str
    description: Optional[str] = None

    goal_id: Optional[int] = None
    difficulty: int = 1
    depends_on_task_id: Optional[int] = None


class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[int] = None


class TaskOut(BaseModel):
    task_id: int
    task_name: str
    description: Optional[str]

    difficulty: int
    percent_completion: float
    achieved: bool

    depends_on_task_id: Optional[int]

    class Config:
        from_attributes = True
