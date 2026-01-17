from datetime import datetime, timezone
from app.services.Analytics.aggregation import aggregate_activities
from app.services.Analytics.primitives import ActivityFilters, AggregationSpec, DateRange
from app.models.enums import SummaryCategoryEnum
from Tests.test_v8_aggregation.seed_activity import seed_activities
import pprint
def test_daily_summary_grouped_by_category(db_session,test_user):
    seed_activities(db_session,test_user.user_id)

    filters = ActivityFilters(
        date_range=DateRange(
            start=datetime(2026, 1, 10, 0, 0, tzinfo=timezone.utc),
            end=datetime(2026, 1, 10, 23, 59, tzinfo=timezone.utc),
        )
    )

    spec = AggregationSpec(
        group_by="summary_category",
        aggregation="sum",
        field="duration_minutes",
    )

    result = aggregate_activities(db_session, filters, spec)
    pprint.pprint(result)
    assert result == {
        SummaryCategoryEnum.learning: 120.0,
        SummaryCategoryEnum.work: 90.0,
        SummaryCategoryEnum.leisure: 30.0,
    }
