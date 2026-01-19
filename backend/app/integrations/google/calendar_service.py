# app/integrations/google/calendar_service.py

from googleapiclient.discovery import build


class GoogleCalendarService:
    def __init__(self, credentials):
        self.service = build("calendar", "v3", credentials=credentials)

    def create_event(self, event_body: dict) -> str:
        event = (
            self.service.events()
            .insert(calendarId="primary", body=event_body)
            .execute()
        )
        return event["id"]

    def update_event(self, calendar_event_id: str, event_body: dict):
        self.service.events().update(
            calendarId="primary",
            eventId=calendar_event_id,
            body=event_body,
        ).execute()

    def delete_event(self, calendar_event_id: str):
        self.service.events().delete(
            calendarId="primary",
            eventId=calendar_event_id
        ).execute()
