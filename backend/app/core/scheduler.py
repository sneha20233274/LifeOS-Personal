from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import SessionLocal
from app.services.reminder_executor import fetch_due_reminders, execute_reminder
from datetime import datetime, timezone
import asyncio
import traceback

scheduler = BackgroundScheduler()


def reminder_job():
    print("⏰ [REMINDER JOB] Tick at", datetime.now(timezone.utc))

    db = SessionLocal()

    try:
        reminders = fetch_due_reminders(db)
        print(f"📦 [REMINDER JOB] Found {len(reminders)} due reminders")

        for reminder in reminders:
            print(
                "🔔 [REMINDER JOB] Executing reminder",
                f"id={reminder.id}",
                f"event={reminder.routine_event_id}",
                f"remind_at={reminder.remind_at}"
            )

            try:
                asyncio.run(execute_reminder(db, reminder))
                print("✅ [REMINDER JOB] Reminder executed:", reminder.id)
            except Exception as e:
                print("❌ [REMINDER JOB] Execution failed:", reminder.id)
                traceback.print_exc()

    except Exception:
        print("❌ [REMINDER JOB] Failed to fetch reminders")
        traceback.print_exc()

    finally:
        db.close()
        print("🔚 [REMINDER JOB] DB session closed")


def start_scheduler():
    print("🚀 Starting reminder scheduler...")

    scheduler.add_job(
        reminder_job,
        trigger="interval",
        seconds=60,
        id="reminder_job",
        replace_existing=True,
    )

    scheduler.start()
    print("✅ Reminder scheduler started")
