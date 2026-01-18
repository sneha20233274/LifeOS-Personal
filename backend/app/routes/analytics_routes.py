from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.models.summary import Summary
from app.schemas.analytics import AnalyticsRequestSchema
from app.core.security import get_current_user


from app.schemas.analytics import AnalyticsRequest
from app.controllers.analytics_controller import run_analytics
 
router = APIRouter(prefix="/analytics", tags=["Summaries"])


@router.get("/summaries/daily")
def get_daily_summary(
    request: Request,
    date_: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
    """
    Returns daily summary for a given date.
    """

    user_id = request.state.user_id

    summary = (
        db.query(Summary)
        .filter(
            Summary.user_id == user_id,
            Summary.summary_type == "daily",
            Summary.period_start == date_,
        )
        .order_by(Summary.created_at.desc())
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Daily summary not found for this date",
        )

    return {
        "date": date_,
        "metrics": summary.metrics,
        "narrative": summary.narrative,
    }


@router.get("/summaries/weekly")
def get_weekly_summary(
    request: Request,
    week_start: date = Query(...),
    db: Session = Depends(get_db),
):
    """
    Returns weekly summary for a given week start date.
    """

    user_id = request.state.user_id

    summary = (
        db.query(Summary)
        .filter(
            Summary.user_id == user_id,
            Summary.summary_type == "weekly",
            Summary.period_start == week_start,
        )
        .order_by(Summary.created_at.desc())
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Weekly summary not found for this week",
        )

    return {
        "week_start": summary.period_start,
        "week_end": summary.period_end,
        "metrics": summary.metrics,
        "narrative": summary.narrative,
    }

@router.get("/summaries/goals")
def get_goal_summaries(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Returns latest goal summaries for the user.
    """

    user_id = request.state.user_id

    summaries = (
        db.query(Summary)
        .filter(
            Summary.user_id == user_id,
            Summary.summary_type == "goal",
        )
        .order_by(Summary.created_at.desc())
        .all()
    )

    if not summaries:
        return []

    return [
        {
            "goal_id": s.goal_id,
            "metrics": s.metrics,
            "narrative": s.narrative,
            "created_at": s.created_at,
        }
        for s in summaries
    ]


@router.get("/summaries/latest")
def get_latest_summaries(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id

    summaries = (
        db.query(Summary)
        .filter(Summary.user_id == user_id)
        .order_by(Summary.created_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "type": s.summary_type,
            "period_start": s.period_start,
            "metrics": s.metrics,
            "narrative": s.narrative,
        }
        for s in summaries
    ]


@router.post("/aggregate")
def aggregate_analytics(
    payload: AnalyticsRequestSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = run_analytics(
        db=db,
        user_id=current_user.user_id,
        request=payload,
    )

    return {
        "data": result
    }

# @router.post("/summary")
# def analytics_summary(
#     payload: ActivityFilters,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     result = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload,
#         spec=AggregationSpec(
#             group_by="summary_category",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     return {
#         "data": result
#     }
# @router.post("/weekday-distribution")
# def weekday_distribution(
#     payload: ActivityFilters,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     result = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload,
#         spec=AggregationSpec(
#             group_by="day_of_week",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     return {
#         "data": result
#     }
# @router.post("/total-time")
# def total_time(
#     payload: ActivityFilters,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     total = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload,
#         spec=AggregationSpec(
#             group_by=None,
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     return {
#         "total_minutes": total
#     }
# from app.services.analytics.visuals import category_distribution
# @router.post("/summary/visual")
# def summary_visual(
#     payload: ActivityFilters,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     aggregated = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload,
#         spec=AggregationSpec(
#             group_by="summary_category",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     return category_distribution(aggregated)
# from app.services.analytics.visuals import weekday_comparison
# @router.post("/weekday/visual")
# def weekday_visual(
#     payload: ActivityFilters,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     aggregated = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload,
#         spec=AggregationSpec(
#             group_by="day_of_week",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     return weekday_comparison(aggregated)

# from app.services.analytics.metrics import compute_productivity
# @router.post("/productivity")
# def productivity(
#     payload: ActivityFilters,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     aggregated = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload,
#         spec=AggregationSpec(
#             group_by="summary_category",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     score = compute_productivity(aggregated)

#     return {
#         "productivity_score": score
#     }
# class ComparisonRequest(BaseModel):
#     current: ActivityFilters
#     previous: ActivityFilters


# from app.services.analytics.comparison import compare_values


# @router.post("/productivity/compare")
# def compare_productivity(
#     payload: ComparisonRequest,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     current_agg = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload.current,
#         spec=AggregationSpec(
#             group_by="summary_category",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     previous_agg = aggregate_activities(
#         db=db,
#         user_id=current_user.user_id,
#         filters=payload.previous,
#         spec=AggregationSpec(
#             group_by="summary_category",
#             aggregation="sum",
#             field="duration_minutes",
#         ),
#     )

#     current_score = compute_productivity(current_agg)
#     previous_score = compute_productivity(previous_agg)

#     return compare_values(current_score, previous_score)
