from datetime import datetime, timezone
from app.models.activity import Activity
from app.models.enums import SummaryCategoryEnum

def seed_activities(db, user_id: int):
    activities = [
        Activity(
            user_id=user_id,
            start_ts=datetime(2026, 1, 10, 10, 0, tzinfo=timezone.utc),
            duration_minutes=120,
            summary_category=SummaryCategoryEnum.learning,
        ),
        Activity(
            user_id=user_id,
            start_ts=datetime(2026, 1, 10, 12, 0, tzinfo=timezone.utc),
            duration_minutes=90,
            summary_category=SummaryCategoryEnum.work,
        ),
        Activity(
            user_id=user_id,
            start_ts=datetime(2026, 1, 10, 15, 0, tzinfo=timezone.utc),
            duration_minutes=30,
            summary_category=SummaryCategoryEnum.leisure,
        ),
        Activity(
            user_id=user_id,
            start_ts=datetime(2026, 1, 11, 11, 0, tzinfo=timezone.utc),
            duration_minutes=60,
            summary_category=SummaryCategoryEnum.learning,
        ),
    ]

    db.add_all(activities)
    db.commit()
