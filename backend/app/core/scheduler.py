from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import get_db
from app.services.reminder_executor import fetch_due_reminders, execute_reminder
import asyncio


scheduler = BackgroundScheduler()


def reminder_job():
    db = get_db()
    reminders = fetch_due_reminders(db)

    for reminder in reminders:
        asyncio.run(execute_reminder(db, reminder))

    db.close()


def start_scheduler():
    scheduler.add_job(
        reminder_job,
        trigger="interval",
        seconds=60,
        id="reminder_job",
        replace_existing=True
    )
    scheduler.start()
