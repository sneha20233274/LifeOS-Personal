# backend/app/schemas/subtask.py

from enum import Enum
from typing import Optional
from datetime import date
from pydantic import BaseModel


class SubtaskType(str, Enum):
    checkbox = "checkbox"     # simple done / not done
    count = "count"           # e.g. solve 50 problems
    duration = "duration"     # e.g. study 600 minutes
    score = "score"           # e.g. score >= 8


class SubtaskCreate(BaseModel):
    subtask_name: str
    task_id: int
    goal_id: Optional[int] = None

    subtask_type: SubtaskType

    target_value: Optional[float] = None
    weight: int = 1

    depends_on_subtask_id: Optional[int] = None
    deadline: Optional[date] = None


class SubtaskUpdate(BaseModel):
    subtask_name: Optional[str] = None
    achieved: Optional[bool] = None
    current_value: Optional[float] = None
    deadline: Optional[date] = None


class SubtaskOut(BaseModel):
    subtask_id: int
    subtask_name: str
    subtask_type: SubtaskType

    achieved: bool
    current_value: float
    target_value: Optional[float]

    weight: int
    deadline: Optional[date]

    class Config:
        from_attributes = True
