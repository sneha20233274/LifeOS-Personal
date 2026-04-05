from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.schemas.reminder import (
    ReminderCreate,
    ReminderResponse,
    ReminderToggle,
)

from app.services.reminder_service import (
    create_reminder,
    list_reminders_for_event,
    delete_reminder,
    create_default_reminder_for_event,
    get_reminder_for_event,
)

router = APIRouter(tags=["Reminders"])


# 🔁 TOGGLE REMINDER (USED BY BELL ICON)
@router.patch(
    "/events/{routine_event_id}/reminder",
    response_model=ReminderResponse | dict,
)
def toggle_reminder(
    routine_event_id: int,
    payload: ReminderToggle,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Toggle reminder for an event.
    - hasReminder = true  → create reminder (if not exists)
    - hasReminder = false → delete reminder (if exists)
    """

    existing = get_reminder_for_event(
        db=db,
        user_id=user.user_id,
        routine_event_id=routine_event_id,
    )

    # 🔕 TURN OFF
    if not payload.hasReminder:
        if existing:
            delete_reminder(db, user.user_id, existing.id)
        return {"hasReminder": False}

    # 🔔 TURN ON
    if existing:
        return existing

    reminder = create_default_reminder_for_event(
        db=db,
        user_id=user.user_id,
        routine_event_id=routine_event_id,
    )

    return reminder


# ➕ CREATE CUSTOM REMINDER (FUTURE UI)
@router.post(
    "/events/{routine_event_id}/reminders",
    response_model=ReminderResponse,
)
def add_reminder(
    routine_event_id: int,
    payload: ReminderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return create_reminder(db, user.user_id, routine_event_id, payload)


# 📋 LIST REMINDERS FOR EVENT
@router.get(
    "/events/{routine_event_id}/reminders",
    response_model=List[ReminderResponse],
)
def list_reminders(
    routine_event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list_reminders_for_event(db, user.user_id, routine_event_id)


# 🗑 DELETE REMINDER
@router.delete(
    "/reminders/{reminder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    delete_reminder(db, user.user_id, reminder_id)
