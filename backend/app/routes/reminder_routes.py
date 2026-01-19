# app/api/routes/reminders.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.reminder import (
    ReminderCreate,
    ReminderResponse
)
from app.services.reminder_service import (
    create_reminder,
    list_reminders_for_event,
    delete_reminder
)

router = APIRouter(tags=["Reminders"])


@router.post(
    "/routine-events/{routine_event_id}/reminders",
    response_model=ReminderResponse
)
def add_reminder(
    routine_event_id: int,
    payload: ReminderCreate,
    db: Session = Depends(get_db),
    user_id: int = 1
):
    return create_reminder(db, user_id, routine_event_id, payload)


@router.get(
    "/routine-events/{routine_event_id}/reminders",
    response_model=List[ReminderResponse]
)
def list_reminders(
    routine_event_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1
):
    return list_reminders_for_event(db, user_id, routine_event_id)


@router.delete(
    "/reminders/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1
):
    delete_reminder(db, user_id, reminder_id)
