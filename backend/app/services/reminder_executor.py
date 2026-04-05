from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.reminder import Reminder
from app.services.email_service import send_reminder_email
from app.models.user import User
import traceback


def fetch_due_reminders(db: Session):
    now = datetime.now(timezone.utc)
    print("🔎 [FETCH] NOW:", now)

    reminders = (
        db.query(Reminder)
        .filter(
            Reminder.status == "scheduled",
            Reminder.remind_at <= now
        )
        .all()
    )

    print("📦 [FETCH] Due reminders:", len(reminders))
    return reminders


async def execute_reminder(
    db: Session,
    reminder: Reminder
):
    print("🔔 [EXECUTE] Reminder", reminder.id)

    try:
        user = db.query(User).filter(User.user_id == reminder.user_id).first()

        if not user or not user.email_id:
            raise RuntimeError("User or email missing")

        if not reminder.routine_event:
            raise RuntimeError("RoutineEvent not loaded")

        print("📧 [EXECUTE] Sending email to", user.email_id)

        await send_reminder_email(
            to_email=user.email_id,
            event=reminder.routine_event
        )

        print("📧 [EXECUTE] Email SUCCESS")

        reminder.status = "sent"
        reminder.sent_at = datetime.now(timezone.utc)

    except Exception:
        print("❌ [EXECUTE] Email FAILED for reminder", reminder.id)
        traceback.print_exc()
        reminder.status = "failed"

    finally:
        db.commit()
        print("💾 [EXECUTE] DB committed, status =", reminder.status)
