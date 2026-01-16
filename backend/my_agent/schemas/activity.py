# backend/app/schemas/activity.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Text
# backend/app/models/enums.py
import enum

class SummaryCategoryEnum(str, enum.Enum):
    work = "work"
    learning = "learning"
    exercise = "exercise"
    admin = "admin"
    leisure = "leisure"
    sleep = "sleep"
    social = "social"
    commute = "commute"
    other = "other"





class ActivityCreate(BaseModel):
    activity_name: str
    activity_description: Optional[str] = None

    start_ts: Optional[datetime] = None
    end_ts: Optional[datetime] = None

    duration_minutes: int = Field(..., gt=0)

    # MUST be one of the enum values
    summary_category: SummaryCategoryEnum

    # semantic only (optional)
    criteria_ids: List[int] = []

class ActivityCreateList(BaseModel):
    activities: List[ActivityCreate]

