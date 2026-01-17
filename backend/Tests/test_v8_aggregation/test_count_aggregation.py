from datetime import datetime, timezone
from app.services.Analytics.aggregation import aggregate_activities
from app.services.Analytics.primitives import ActivityFilters, AggregationSpec, DateRange
from Tests.test_v8_aggregation.seed_activity import seed_activities
def test_count_activities(db_session,test_user):
    seed_activities(db_session,test_user.user_id)

    filters = ActivityFilters(
        date_range=DateRange(
            start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            end=datetime(2026, 1, 31, tzinfo=timezone.utc),
        )
    )

    spec = AggregationSpec(
        group_by=None,
        aggregation="count",
    )

    result = aggregate_activities(db_session, filters, spec)
  
    assert result == 4
