from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional, List, Literal
from app.models.enums import SummaryCategoryEnum

@dataclass
class DateRange:
    start: date
    end: date

@dataclass
class ActivityFilters:
    date_range: DateRange
    day_of_week: Optional[List[int]] = None  # 0=Mon ... 6=Sun
    summary_category: Optional[List[SummaryCategoryEnum]] = None
    subtask_id: Optional[int] = None
    task_id: Optional[int] = None
    goal_id: Optional[int] = None

AggregationType = Literal["sum", "count", "average"]

@dataclass
class AggregationSpec:
    group_by: Optional[str]          # e.g. "summary_category", "day_of_week"
    aggregation: AggregationType     # sum | count | average
    field: Optional[str] = None      # e.g. "duration_minutes"


