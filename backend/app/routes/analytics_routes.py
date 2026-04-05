# app/routes/analytics_routes.py

from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.models.summary import Summary
from app.core.security import get_current_user
from app.schemas.analytics import AnalyticsRequest
from app.controllers.analytics_controller import run_analytics
from app.services.Analytics.metrics import compute_productivity
from app.services.Analytics.visuals import weekday_comparison
from app.services.Analytics.comparison import rolling_average
from app.services.Analytics.insights import generate_insights
from app.services.Analytics.primitives import AggregationSpec
from app.services.Analytics.aggregation import aggregate_activities
# app/schemas/insights.py

from pydantic import BaseModel
from app.services.Analytics.primitives import ActivityFilters

class InsightsRequest(BaseModel):
    filters: ActivityFilters

router = APIRouter(tags=["Analytics"])


@router.post("/aggregate")
def aggregate_analytics(payload: AnalyticsRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = run_analytics(
        db=db,
        user_id=current_user.user_id,
        request=payload,
    )

    formatted = [
        {
            "name": str(category.value),  # enum → string
            "value": round(value, 2)
        }
        for category, value in result.items()
    ]

    return { "data": formatted }


from app.models.enums import productive_categories

@router.post("/weekly")
def weekly_distribution(payload: AnalyticsRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = run_analytics(
        db=db,
        user_id=current_user.user_id,
        request=payload,
    )

    formatted = []

    for day, total in result.items():
        try:
            day_int = int(day)
        except:
            continue

        productive = sum(
            v for k, v in result.items()
            if k in productive_categories
        )

        formatted.append({
            "day": day_int,
            "productive": round(productive / 60, 2),
            "nonProductive": round((total - productive) / 60, 2),
        })

    return { "data": formatted }
@router.post("/trend")
def productivity_trend(payload: AnalyticsRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    aggregated = run_analytics(
        db=db,
        user_id=current_user.user_id,
        request=payload,
    )

    formatted = []

    for day, value in aggregated.items():
        try:
            formatted.append({
                "day": int(day),
                "score": round(value, 2)
            })
        except:
            continue

    return { "data": sorted(formatted, key=lambda x: x["day"]) }

 

@router.post("/insights")
def get_insights(
    payload: InsightsRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user), 
):
    
    user_id = user.user_id  

    category = aggregate_activities(
        db,
        user_id,
        payload.filters,
        AggregationSpec(
            group_by="summary_category",
            aggregation="sum",
            field="duration_minutes"
        )
    )

    weekday = aggregate_activities(
        db,
        user_id,
        payload.filters,
        AggregationSpec(
            group_by="day_of_week",
            aggregation="sum",
            field="duration_minutes"
        )
    )

    productivity = compute_productivity(category)

    insights = generate_insights(
        category,
        weekday,
        [productivity]
    )

    return {"insights": insights}

@router.get("/summaries/daily")
def get_daily_summary(
    request: Request,
    date_: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
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
@router.post("/productivity")
def get_productivity(
    payload: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    aggregated = run_analytics(
        db=db,
        user_id=current_user.user_id,
        request=payload,
    )

    

    score = compute_productivity(aggregated)

    return {
    "score": round(score * 100, 2)
}
@router.post("/productivity-average")
def productivity_average(
    payload: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # aggregated is already a float
    aggregated = run_analytics(
        db=db,
        user_id=current_user.user_id,
        request=payload,
    )

    # no .values() needed
    avg = rolling_average([aggregated])  # wrap in list if rolling_average expects iterable

    return {
        "average": round(avg, 2)
    }