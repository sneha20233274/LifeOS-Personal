# backend/app/crud/activity.py
# backend/app/crud/activity.py
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict
from datetime import datetime

from app.models.activity import Activity
from app.models.criteria import Criteria
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.models.enums import SummaryCategoryEnum


def create_activity(
    db: Session,
    user_id: int,
    obj_in: ActivityCreate
) -> Activity:
    """
    Creates a new activity.
    Activity may or may not belong to a subtask.
    Time is counted ONLY via summary_category.
    """

    db_obj = Activity(
        user_id=user_id,
        subtask_id=obj_in.subtask_id,
        activity_name=obj_in.activity_name,
        activity_description=obj_in.activity_description,
        start_ts=obj_in.start_ts,
        end_ts=obj_in.end_ts,
        duration_minutes=obj_in.duration_minutes,
        summary_category=obj_in.summary_category,
        app_name=obj_in.app_name,
        domain=obj_in.domain,
        device=obj_in.device,
        source=obj_in.source,
        focus_score=obj_in.focus_score,
    )

    # attach criteria (semantic only)
    if obj_in.criteria_ids:
        criteria = (
            db.query(Criteria)
            .filter(Criteria.criteria_id.in_(obj_in.criteria_ids))
            .all()
        )
        db_obj.criteria = criteria

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
def get_activity(db: Session, activity_id: int) -> Optional[Activity]:
    return (
        db.query(Activity)
        .filter(Activity.activity_id == activity_id)
        .first()
    )

def get_user_activities_in_period(
    db: Session,
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    limit: int = 500
) -> List[Activity]:
    """
    Returns at most `limit` activities of a user within a period.
    If more exist, most recent ones are returned.
    """

    return (
        db.query(Activity)
        .filter(
            Activity.user_id == user_id,
            Activity.start_ts >= start_date,
            Activity.start_ts <= end_date,
        )
        .order_by(desc(Activity.start_ts))
        .limit(limit)
        .all()
    )
def get_subtask_activities_by_duration(
    db: Session,
    subtask_id: int,
    min_duration_minutes: int
) -> List[Activity]:
    """
    Returns activities linked to a subtask
    whose duration is >= min_duration_minutes.
    """

    return (
        db.query(Activity)
        .filter(
            Activity.subtask_id == subtask_id,
            Activity.duration_minutes >= min_duration_minutes,
        )
        .order_by(desc(Activity.start_ts))
        .all()
    )
def update_activity(
    db: Session,
    activity_id: int,
    obj_in: ActivityUpdate
) -> Optional[Activity]:

    db_obj = get_activity(db, activity_id)
    if not db_obj:
        return None

    update_data = obj_in.dict(exclude_unset=True)

    # criteria handling
    if "criteria_ids" in update_data:
        criteria = (
            db.query(Criteria)
            .filter(Criteria.criteria_id.in_(update_data["criteria_ids"]))
            .all()
        )
        db_obj.criteria = criteria
        update_data.pop("criteria_ids")

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj
def delete_activity(db: Session, activity_id: int) -> bool:
    db_obj = get_activity(db, activity_id)
    if not db_obj:
        return False

    db.delete(db_obj)
    db.commit()
    return True





def get_time_spent_by_summary_category(
    db: Session,
    user_id: int,
    start_date: datetime,
    end_date: datetime
) -> Dict[SummaryCategoryEnum, int]:
    """
    Returns total time spent per summary_category.
    This is the PRIMARY input for AI feedback.
    """

    rows = (
        db.query(
            Activity.summary_category,
            func.sum(Activity.duration_minutes)
        )
        .filter(
            Activity.user_id == user_id,
            Activity.start_ts >= start_date,
            Activity.start_ts <= end_date,
        )
        .group_by(Activity.summary_category)
        .all()
    )

    return {category: total for category, total in rows}

def get_time_spent_by_criteria(
    db: Session,
    user_id: int,
    start_date: datetime,
    end_date: datetime
) -> Dict[str, int]:
    """
    Returns time spent grouped by criteria (semantic labels).
    Used for drill-downs, goals, and AI insights.
    """

    rows = (
        db.query(
            Criteria.name,
            func.sum(Activity.duration_minutes)
        )
        .join(Activity.criteria)
        .filter(
            Activity.user_id == user_id,
            Activity.start_ts >= start_date,
            Activity.start_ts <= end_date,
        )
        .group_by(Criteria.name)
        .all()
    )

    return {name: total for name, total in rows}

def get_activities_by_user(db, user_id, skip, limit):
    return (
        db.query(Activity)
        .filter(Activity.user_id == user_id)
        .order_by(Activity.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
