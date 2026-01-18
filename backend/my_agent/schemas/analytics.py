# schemas/aggregation_schema.py
from pydantic import BaseModel
from typing import Union, Literal, Optional, List
from datetime import date

class DateRange(BaseModel):
    start: date
    end: date

class AggregationSpec(BaseModel):
    date_range: DateRange
    day_of_week: Optional[List[int]] = None
    summary_category: Optional[List[str]] = None

    aggregation: Literal["sum", "count", "average"]
    field: Literal["duration_minutes"]
    group_by: Optional[
        Literal["summary_category", "day_of_week", "date"]
    ] = None

class NoAggregation(BaseModel):
    type: Literal["none"] = "none"

# schemas/aggregation_schema.py
from pydantic import BaseModel
from typing import Literal, Optional, List
from datetime import date


class DateRange(BaseModel):
    start: date
    end: date


class AggregationSpec(BaseModel):
    date_range: DateRange
    day_of_week: Optional[List[int]] = None
    summary_category: Optional[List[str]] = None

    aggregation: Literal["sum", "count", "average"]
    field: Literal["duration_minutes"]
    group_by: Optional[
        Literal["summary_category", "day_of_week", "date"]
    ] = None


class AggregationOutput(BaseModel):
    """
    Single tool-safe output schema.

    - type = "none" → no aggregation requested
    - type = "aggregation" → aggregation_spec is present
    """
    type: Literal["aggregation", "none"]

    aggregation: Optional[AggregationSpec] = None

