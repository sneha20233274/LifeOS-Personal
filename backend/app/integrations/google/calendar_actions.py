# app/integrations/google/calendar_actions.py

from sqlalchemy.orm import Session
from app.integrations.google.credentials import get_credentials_for_user
from app.integrations.google.calendar_service import GoogleCalendarService
from app.models.routine_event import RoutineEvent


def build_event_body(routine_event: RoutineEvent) -> dict:
    return {
        "summary": routine_event.title,
        "description": routine_event.description or "",
        "start": {
            "dateTime": routine_event.start_time.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": routine_event.end_time.isoformat(),
            "timeZone": "UTC",
        },
    }


def push_create_event(
    db: Session,
    user_id: int,
    routine_event: RoutineEvent,
):
    creds = get_credentials_for_user(db, user_id)
    if not creds:
        return None  # user not connected

    calendar = GoogleCalendarService(creds)
    event_body = build_event_body(routine_event)

    calendar_event_id = calendar.create_event(event_body)
    return calendar_event_id


def push_update_event(
    db: Session,
    user_id: int,
    routine_event: RoutineEvent,
):
    if not routine_event.calendar_event_id:
        return

    creds = get_credentials_for_user(db, user_id)
    if not creds:
        return

    calendar = GoogleCalendarService(creds)
    event_body = build_event_body(routine_event)

    calendar.update_event(routine_event.calendar_event_id, event_body)


def push_delete_event(
    db: Session,
    user_id: int,
    routine_event: RoutineEvent,
):
    if not routine_event.calendar_event_id:
        return

    creds = get_credentials_for_user(db, user_id)
    if not creds:
        return

    calendar = GoogleCalendarService(creds)
    calendar.delete_event(routine_event.calendar_event_id)
