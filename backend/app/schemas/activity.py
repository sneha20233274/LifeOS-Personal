# backend/app/schemas/activity.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActivityCreate(BaseModel):
    activity_name: str
    activity_description: Optional[str] = None
    estimated_minutes: Optional[int] = 0
    subtask_id: Optional[int] = None

class ActivityOut(BaseModel):
    activity_id: int
    user_id: int
    activity_name: str
    created_at: datetime

    class Config:
        orm_mode = True
