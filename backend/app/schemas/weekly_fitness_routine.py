from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from enum import Enum


class RoutineStatus(str, Enum):
    draft = "draft"
    approved = "approved"


class WeeklyFitnessRoutineResponse(BaseModel):
    routine_id: str
    user_id: str
    routine_name: str

    # 🔥 EXACT LLM OUTPUT — DO NOT TRANSFORM
    plan_snapshot: Dict[str, Any]
    schedule: Dict[str, Any]

    status: RoutineStatus
    created_at: datetime

    class Config:
        orm_mode = True
