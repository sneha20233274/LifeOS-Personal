# app/services/analytics/execution.py

from sqlalchemy import func
from app.models.activity import Activity


def execution_quality(db, user_id, start, end):
    total = db.query(func.count(Activity.activity_id)).filter(
        Activity.user_id == user_id,
        Activity.start_ts.between(start, end)
    ).scalar()

    completed = db.query(func.count(Activity.activity_id)).filter(
        Activity.user_id == user_id,
        Activity.start_ts.between(start, end),
        Activity.subtask_id.isnot(None)
    ).scalar()

    return {
        "total_activities": total or 0,
        "completed_activities": completed or 0,
        "completion_ratio": (completed / total) if total else 0.0
    }
