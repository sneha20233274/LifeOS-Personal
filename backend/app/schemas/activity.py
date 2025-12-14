# backend/app/schemas/activity.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.enums import SummaryCategoryEnum
from sqlalchemy import Text

class CriteriaOut(BaseModel):
    criteria_id: int
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True


class ActivityCreate(BaseModel):
    activity_name: str
    activity_description: Optional[str] = None

    start_ts: Optional[datetime]
    end_ts: Optional[datetime]

    duration_minutes: int = Field(..., gt=0)

    summary_category: SummaryCategoryEnum

    # semantic only
    criteria_ids: List[int] = []

    subtask_id: Optional[int] = None

    app_name: Optional[str]
    domain: Optional[str]
    device: Optional[str]
    source: Optional[str]
    focus_score: Optional[float]


class ActivityUpdate(BaseModel):
    activity_name: Optional[str]
    activity_description: Optional[str]

    start_ts: Optional[datetime]
    end_ts: Optional[datetime]
    duration_minutes: Optional[int]

    summary_category: Optional[SummaryCategoryEnum]
    criteria_ids: Optional[List[int]]
    subtask_id: Optional[int]

    app_name: Optional[str]
    domain: Optional[str]
    device: Optional[str]
    source: Optional[str]
    focus_score: Optional[float]


class ActivityOut(BaseModel):
    activity_id: int
    user_id: int
    subtask_id: Optional[int]

    activity_name: str
    activity_description: Optional[str]

    start_ts: Optional[datetime]
    end_ts: Optional[datetime]
    duration_minutes: int

    summary_category: SummaryCategoryEnum
    criteria: List[CriteriaOut]

    created_at: datetime

    class Config:
        orm_mode = True
