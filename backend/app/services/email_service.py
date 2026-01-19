from fastapi_mail import MessageSchema
from app.core.email import fastmail


async def send_reminder_email(
    to_email: str,
    title: str,
    start_time
):
    message = MessageSchema(
        subject=f"Reminder: {title}",
        recipients=[to_email],
        body=f"You have an upcoming routine at {start_time}",
        subtype="plain"
    )

    await fastmail.send_message(message)
