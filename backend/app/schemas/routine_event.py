# app/schemas/routine_event.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class PriorityEnum(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"


class StatusEnum(str, Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    skipped = "Skipped"


class SourceEnum(str, Enum):
    manual = "manual"
    ai = "ai"
    imported = "imported"
    system = "system"


class RoutineEventCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    start_time: datetime
    end_time: datetime
    is_all_day: bool = False

    category: str = "General"
    priority: PriorityEnum = PriorityEnum.medium
    status: StatusEnum = StatusEnum.scheduled

    location_or_link: Optional[str] = None
    source: SourceEnum = SourceEnum.manual


class RoutineEventResponse(RoutineEventCreate):
    id: int
    user_id: int
    calendar_event_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




class RoutineEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_all_day: Optional[bool] = None

    category: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None

    location_or_link: Optional[str] = None
