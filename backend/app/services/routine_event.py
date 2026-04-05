from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime , timedelta
from app.models.routine_event import RoutineEvent
from app.schemas.routine_event import RoutineEventCreate, RoutineEventUpdate
from app.integrations.google.calendar_actions import (
    push_create_event,
    push_update_event,
    push_delete_event,
)
from sqlalchemy import case,and_
from app.models.reminder import Reminder

def get_routine_event(
    db: Session,
    user_id: int,
    event_id: int
) -> RoutineEvent:

    event = (
        db.query(RoutineEvent)
        .filter(
            RoutineEvent.id == event_id,
            RoutineEvent.user_id == user_id
        )
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="RoutineEvent not found")

    return event

def list_routine_events(
    db: Session,
    user_id: int
):
    return (
        db.query(RoutineEvent)
        .filter(RoutineEvent.user_id == user_id)
        .order_by(RoutineEvent.start_time.asc())
        .all()
    )

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
from app.models.routine_event import RoutineEvent

def list_routine_events_by_date(
    db,
    user_id: int,
    date: datetime,
    tz: str,
):
    """
    date: UTC datetime that represents LOCAL midnight
    tz: IANA timezone string (e.g. 'Asia/Kolkata', 'America/New_York')
    """

    user_tz = ZoneInfo(tz)

    # 1️⃣ Convert UTC → user's local timezone
    local_date = date.astimezone(user_tz)

    # 2️⃣ Build local day range
    local_start = local_date.replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    local_end = local_start + timedelta(days=1)

    # 3️⃣ Convert back to UTC
    utc_start = local_start.astimezone(ZoneInfo("UTC"))
    utc_end = local_end.astimezone(ZoneInfo("UTC"))

    # 4️⃣ Query events + reminder state (USER-SCOPED)
    rows = (
        db.query(
            RoutineEvent,
            case(
                (Reminder.id.isnot(None), True),
                else_=False
            ).label("has_reminder")
        )
        .outerjoin(
            Reminder,
            and_(
                Reminder.routine_event_id == RoutineEvent.id,
                Reminder.user_id == user_id,   # 🔥 THIS FIXES IT
            )
        )
        .filter(
            RoutineEvent.user_id == user_id,
            RoutineEvent.start_time >= utc_start,
            RoutineEvent.start_time < utc_end,
        )
        .order_by(RoutineEvent.start_time.asc())
        .all()
    )

    events = []
    for event, has_reminder in rows:
        event.has_reminder = has_reminder
        events.append(event)
    print([(e.id, e.has_reminder) for e in events])

    return events


def create_routine_event(
    db: Session,
    user_id: int,
    payload: RoutineEventCreate,
) -> RoutineEvent:

    if payload.end_time <= payload.start_time:
        raise HTTPException(
            status_code=400,
            detail="end_time must be after start_time"
        )

    event = RoutineEvent(
        user_id=user_id,
        **payload.model_dump()
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    # 🔹 Push to Google Calendar (non-blocking)
    try:
        calendar_event_id = push_create_event(db, user_id, event)
        if calendar_event_id:
            event.calendar_event_id = calendar_event_id
            db.commit()
            db.refresh(event)
    except Exception as e:
        # Log only — never break core flow
        print("Google create failed:", e)

    return event


def update_routine_event(
    db: Session,
    user_id: int,
    event_id: int,
    payload: RoutineEventUpdate,
) -> RoutineEvent:

    event = get_routine_event(db, user_id, event_id)

    update_data = payload.model_dump(exclude_unset=True)

    if "start_time" in update_data or "end_time" in update_data:
        start = update_data.get("start_time", event.start_time)
        end = update_data.get("end_time", event.end_time)

        if end <= start:
            raise HTTPException(
                status_code=400,
                detail="end_time must be after start_time"
            )

    for key, value in update_data.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    # 🔹 Push update to Google Calendar
    try:
        push_update_event(db, user_id, event)
    except Exception as e:
        print("Google update failed:", e)

    return event

def delete_routine_event(
    db: Session,
    user_id: int,
    event_id: int,
):
    event = get_routine_event(db, user_id, event_id)

    # 🔹 Push delete BEFORE DB delete
    try:
        push_delete_event(db, user_id, event)
    except Exception as e:
        print("Google delete failed:", e)

    db.delete(event)
    db.commit()
