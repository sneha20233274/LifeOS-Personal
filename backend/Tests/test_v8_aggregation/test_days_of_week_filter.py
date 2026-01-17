from datetime import datetime, timezone
from app.services.Analytics.aggregation import aggregate_activities
from app.services.Analytics.primitives import ActivityFilters, AggregationSpec, DateRange
from Tests.test_v8_aggregation.seed_activity import seed_activities
def test_filter_by_day_of_week(db_session,test_user):
    seed_activities(db_session,test_user.user_id)

    filters = ActivityFilters(
        date_range=DateRange(
            start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            end=datetime(2026, 1, 31, tzinfo=timezone.utc),
        ),
        day_of_week=[6],  # Saturday
    )

    spec = AggregationSpec(
        group_by=None,
        aggregation="sum",
        field="duration_minutes",
    )

    result = aggregate_activities(db_session, filters, spec)
    print(result)
    assert result == 240.0
