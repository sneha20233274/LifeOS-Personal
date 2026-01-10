from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.core.database import get_db
from app.models.summary import Summary

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
