from datetime import date
from typing import Optional, List, Literal
from pydantic import BaseModel
from app.models.enums import SummaryCategoryEnum

class DateRange(BaseModel):
    start: date
    end: date


class ActivityFilters(BaseModel):
    date_range: DateRange
    day_of_week: Optional[List[int]] = None
    summary_category: Optional[List[SummaryCategoryEnum]] = None
    subtask_id: Optional[int] = None
    # task_id: Optional[int] = None
    # goal_id: Optional[int] = None

AggregationType = Literal["sum", "count", "average"]


class AggregationSpec(BaseModel):
    group_by: Optional[str] = None   # "summary_category", "day_of_week"
    aggregation: AggregationType
    field: Optional[str] = None      # "duration_minutes"


class AnalyticsRequest(BaseModel):
    filters: ActivityFilters
    spec: AggregationSpec
