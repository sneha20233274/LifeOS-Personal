# app/services/reminder_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.reminder import Reminder
from app.models.routine_event import RoutineEvent
from app.schemas.reminder import ReminderCreate


def create_reminder(
    db: Session,
    user_id: int,
    routine_event_id: int,
    payload: ReminderCreate | None = None
) -> Reminder:
    
    event = (
        db.query(RoutineEvent)
        .filter(
            RoutineEvent.id == routine_event_id,
            RoutineEvent.user_id == user_id
        )
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="RoutineEvent not found")

    remind_at = payload.remind_at if payload else event.start_time

    if remind_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="remind_at cannot be in the past"
        )

    reminder = Reminder(
        routine_event_id=routine_event_id,
        user_id=user_id,
        remind_at=remind_at,
        channel=payload.channel if payload else "email"
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


def list_reminders_for_event(
    db: Session,
    user_id: int,
    routine_event_id: int
):
    return (
        db.query(Reminder)
        .filter(
            Reminder.user_id == user_id,
            Reminder.routine_event_id == routine_event_id
        )
        .order_by(Reminder.remind_at.asc())
        .all()
    )


def delete_reminder(
    db: Session,
    user_id: int,
    reminder_id: int
):
    reminder = (
        db.query(Reminder)
        .filter(
            Reminder.id == reminder_id,
            Reminder.user_id == user_id
        )
        .first()
    )

    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()
