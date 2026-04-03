from sqlalchemy.orm import Session
from app.schemas.analytics import AnalyticsRequest
from app.services.Analytics.aggregation import aggregate_activities


def run_analytics(
    db: Session,
    user_id: int,
    request: AnalyticsRequest,
):
    return aggregate_activities(
        db=db,
        filters=request.filters,
        spec=request.spec,
        user_id=user_id,
    )
