from fastapi_mail import MessageSchema
from app.core.email import fastmail

from datetime import timezone

from datetime import timezone

def build_reminder_context(event):
    start = event.start_time.astimezone(timezone.utc)

    end = (
        event.end_time.astimezone(timezone.utc)
        if event.end_time
        else None
    )

    return {
        "title": event.title or "Untitled Event",

        "description": event.description or "No description provided.",

        "start_time": start.strftime("%d %b %Y, %I:%M %p UTC"),

        "end_time": (
            end.strftime("%I:%M %p UTC") if end else "Not specified"
        ),

        "category": event.category or "General",

        "priority": event.priority or "Normal",

        "location": event.location_or_link or None,

        "is_all_day": bool(event.is_all_day),
    }
  


def build_email_body(ctx: dict) -> str:
    lines = [
        f"🔔 Reminder: {ctx['title']}",
        "",
        f"🕒 When: {ctx['start_time']} – {ctx['end_time']}",
    ]

    if ctx["location"]:
        lines.append(f"📍 Location / Link: {ctx['location']}")

    lines.extend([
        f"📂 Category: {ctx['category']}",
        f"⚡ Priority: {ctx['priority']}",
        "",
        f"📝 Notes:",
        ctx["description"],
        "",
        "— LifeOS",
    ])

    return "\n".join(lines)


async def send_reminder_email(
    to_email: str,
    event
):
    ctx = build_reminder_context(event)
    body = build_email_body(ctx)

    message = MessageSchema(
        subject=f"🔔 Reminder: {ctx['title']}",
        recipients=[to_email],
        body=body,
        subtype="plain"
    )

    await fastmail.send_message(message)
