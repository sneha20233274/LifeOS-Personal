# backend/app/services/analytics/time.py

from sqlalchemy import func
from app.models.activity import Activity
from app.services.Analytics.core import PRODUCTIVE_CATEGORIES


def time_distribution(db, user_id, start, end):
    """
    Minutes per summary category.
    """
    rows = (
        db.query(
            Activity.summary_category,
            func.sum(Activity.duration_minutes).label("minutes")
        )
        .filter(
            Activity.user_id == user_id,
            Activity.start_ts.between(start, end)
        )
        .group_by(Activity.summary_category)
        .all()
    )
    
    return {r.summary_category.value: r.minutes for r in rows}


def productive_minutes(db, user_id, start, end) -> int:
    """
    Total productive minutes.
    """
    return (
        db.query(func.sum(Activity.duration_minutes))
        .filter(
            Activity.user_id == user_id,
            Activity.summary_category.in_(PRODUCTIVE_CATEGORIES),
            Activity.start_ts.between(start, end)
        )
        .scalar()
    ) or 0
