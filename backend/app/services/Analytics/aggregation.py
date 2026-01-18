from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.activity import Activity
from app.services.Analytics.primitives import ActivityFilters, AggregationSpec


def aggregate_activities(
    db: Session,
    user_id:int,
    filters: ActivityFilters,
    spec: AggregationSpec,
) -> Dict[Any, float] | float:
    """
    Generic aggregation over activities.

    Supports:
    - filtering (date range, derived weekday, category, subtask)
    - grouping
    - sum / count / average

    Returns:
    - dict when group_by is provided
    - scalar when no group_by
    """

    q = db.query(Activity)
    q = q.filter(Activity.user_id == user_id)
    # ---------------------------
    # Date filter (AUTHORITATIVE)
    # ---------------------------
    q = q.filter(
        Activity.start_ts >= filters.date_range.start,
        Activity.start_ts <= filters.date_range.end,
    )

    # ---------------------------
    # Derived weekday filter
    # PostgreSQL: 0=Sunday ... 6=Saturday
    # ---------------------------
    if filters.day_of_week:
        q = q.filter(
            extract("dow", Activity.start_ts).in_(filters.day_of_week)
        )

    # ---------------------------
    # Direct column filters
    # ---------------------------
    if filters.summary_category:
        q = q.filter(Activity.summary_category.in_(filters.summary_category))

    if filters.subtask_id is not None:
        q = q.filter(Activity.subtask_id == filters.subtask_id)

    # (task_id, goal_id can be added later when model supports them)

    # ---------------------------
    # Aggregation function
    # ---------------------------
    if spec.aggregation == "sum":
        agg_fn = func.sum(getattr(Activity, spec.field))

    elif spec.aggregation == "count":
        agg_fn = func.count(Activity.activity_id)

    elif spec.aggregation == "average":
        agg_fn = func.avg(getattr(Activity, spec.field))

    else:
        raise ValueError(f"Unsupported aggregation: {spec.aggregation}")

    # ---------------------------
    # Grouping
    # ---------------------------
    if spec.group_by:
        if spec.group_by == "day_of_week":
            group_col = extract("dow", Activity.start_ts)
        else:
            group_col = getattr(Activity, spec.group_by)

        rows = (
            q.with_entities(group_col.label("group_key"), agg_fn)
             .group_by(group_col)
             .all()
        )

        return {key: float(value or 0) for key, value in rows}

    # ---------------------------
    # Scalar result
    # ---------------------------
    value = q.with_entities(agg_fn).scalar()
    return float(value or 0)
