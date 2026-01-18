# app/tools/analytics_tools.py

from typing import Optional, List, Literal, Dict
from datetime import date
from langchain.tools import tool
from pydantic import BaseModel, Field

# --- Import Internal Services & Models ---
from app.core.database import get_db
from app.models.enums import SummaryCategoryEnum

# Service Logic Imports
from app.services.Analytics.execution import execution_quality
from app.services.Analytics.criteria import criteria_breakdown
from app.services.Analytics.aggregation import aggregate_activities
from app.services.Analytics.primitives import ActivityFilters, AggregationSpec, DateRange
from app.services.Analytics.metrics import compute_productivity, compute_total_time
from app.services.Analytics.comparison import compare_values, rolling_average, variance


# =============================================================================
#  DATABASE TOOLS (Require DB Session)
# =============================================================================

@tool
def check_execution_quality(start_date: str, end_date: str,**kwargs):
    
    """
    Calculates the completion ratio of planned tasks vs. total activities.
    Use this to see if the user is sticking to their schedule/plan.
    
    Args:
        user_id: The ID of the user.
        start_date: Start date in 'YYYY-MM-DD' format.
        end_date: End date in 'YYYY-MM-DD' format.
    """
    user_id = kwargs.get("user_id")
    db = get_db()
    try:
        # Convert string dates (from Agent) to Python Date objects (for Service)
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        
        return execution_quality(db, user_id, start, end)
    finally:
        db.close()


@tool
def get_criteria_breakdown(user_id: int, start_date: str, end_date: str,**kwargs):
    """
    Returns a breakdown of time spent on different criteria (tags).
    Useful for visualizing specific focus areas like 'Deep Work' vs 'Shallow Work'.
    
    Args:
        user_id: The ID of the user.
        start_date: Start date in 'YYYY-MM-DD' format.
        end_date: End date in 'YYYY-MM-DD' format.
    """
    db = get_db()
    user_id = kwargs.get("user_id")
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        
        return criteria_breakdown(db, user_id, start, end)
    finally:
        db.close()


# --- Aggregation Tool Schema ---

class AggregationInput(BaseModel):
  
    start_date: str = Field(..., description="YYYY-MM-DD")
    end_date: str = Field(..., description="YYYY-MM-DD")
    group_by: Optional[str] = Field(None, description="Field to group by: 'summary_category' or 'day_of_week'")
    aggregation_type: Literal["sum", "count", "average"] = Field("sum", description="Type of calculation")
    field_to_aggregate: str = Field("duration_minutes", description="Field to measure, usually 'duration_minutes'")

@tool(args_schema=AggregationInput)
def analyze_activities(
    start_date: str, 
    end_date: str, 
    group_by: Optional[str] = None, 
    aggregation_type: str = "sum", 
    field_to_aggregate: str = "duration_minutes",
    **kwargs
):
    """
    Advanced analytics tool. Use this to sum duration, count activities, or find averages.
    Can group data by category or day of week.
    Example: "Total time spent on work last week" -> sum duration grouped by summary_category.
    """
    user_id = kwargs.get("user_id")
    db = get_db()
    try:
        # Reconstruct Service Primitives
        date_range = DateRange(
            start=date.fromisoformat(start_date),
            end=date.fromisoformat(end_date)
        )
        
        filters = ActivityFilters(
            date_range=date_range,
            # Note: Ensure your ActivityFilters definition in primitives.py 
            # actually supports user_id if you want to filter by user here.
            # user_id=user_id 
        )

        spec = AggregationSpec(
            group_by=group_by,
            aggregation=aggregation_type,
            field=field_to_aggregate
        )

        return aggregate_activities(db,user_id, filters, spec)
    finally:
        db.close()


# =============================================================================
#  MATH / METRIC TOOLS (Pure Logic)
# =============================================================================

# --- Productivity Tool Schema ---

class ProductivityInput(BaseModel):
    category_data: Dict[SummaryCategoryEnum, float] = Field(
        ..., 
        description=(
            "A dictionary where keys are categories and values are minutes. "
            "Keys MUST be one of: work, learning, exercise, admin, leisure, "
            "sleep, social, health, commute, other."
        )
    )

@tool(args_schema=ProductivityInput)
def calculate_productivity_score(category_data: Dict[SummaryCategoryEnum, float]) -> float:
    """
    Calculates the productivity score (0.0 to 1.0) based on time spent per category.
    The input should be the result of an aggregation query grouped by category.
    """
    # The Pydantic schema guarantees we get Enums.
    # We convert keys to values (strings) just in case the service expects raw strings.
    # If compute_productivity handles Enums directly, you can remove the list comprehension.
    cleaned_data = {k.value: v for k, v in category_data.items()}
    
    return compute_productivity(cleaned_data)


@tool
def calculate_total_time(category_data: Dict[str, float]) -> float:
    """
    Simple tool to sum up total minutes from a dictionary of categories.
    """
    return compute_total_time(category_data)


# --- Comparison Tools ---

@tool
def analyze_trend(current: float, previous: float) -> dict:
    """
    Compares two metric values to determine the trend (improving/declining) and delta.
    Use this when the user asks "Am I doing better than last week?".
    
    Args:
        current: The value for the current period.
        previous: The value for the previous period.
    """
    return compare_values(current, previous)

@tool
def calculate_variance(values: List[float]) -> float:
    """
    Calculates the variance of a list of numbers. 
    Useful for checking consistency (e.g., "Was my sleep schedule consistent?").
    """
    return variance(values)

@tool
def calculate_average(values: List[float]) -> float:
    """
    Calculates the rolling average of a list of numbers.
    """
    return rolling_average(values)