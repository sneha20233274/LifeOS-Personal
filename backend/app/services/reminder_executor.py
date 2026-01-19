from datetime import datetime
from sqlalchemy.orm import Session
from app.models.reminder import Reminder
from app.services.email_service import send_reminder_email
from app.models.user import User
import asyncio


def fetch_due_reminders(db: Session):
    return (
        db.query(Reminder)
        .filter(
            Reminder.status == "scheduled",
            Reminder.remind_at <= datetime.utcnow()
        )
        .all()
    )


async def execute_reminder(
    db: Session,
    reminder: Reminder
):
    try:
        user = db.query(User).filter(User.id == reminder.user_id).first()

        await send_reminder_email(
            to_email=user.email,
            title=reminder.routine_event.title,
            start_time=reminder.routine_event.start_time
        )

        reminder.status = "sent"
        reminder.sent_at = datetime.utcnow()

    except Exception as e:
        reminder.status = "failed"

    finally:
        db.commit()
