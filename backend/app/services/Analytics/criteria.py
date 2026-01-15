# app/services/analytics/criteria.py
from sqlalchemy import func
from app.models.criteria import Criteria
from app.models.activity import Activity, activity_criteria

def criteria_breakdown(db, user_id, start, end):
    rows = (
        db.query(
            Criteria.name,
            func.sum(Activity.duration_minutes).label("minutes")
        )
        .join(activity_criteria)
        .join(Activity)
        .filter(
            Activity.user_id == user_id,
            Activity.start_ts.between(start, end)
        )
        .group_by(Criteria.name)
        .order_by(func.desc("minutes"))
        .all()
    )
    return {r.name: r.minutes for r in rows}
