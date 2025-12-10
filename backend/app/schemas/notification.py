# backend/app/schemas/habit.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    target_minutes: Optional[int] = 0

class HabitOut(BaseModel):
    habit_id: int
    user_id: int
    name: str
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True
