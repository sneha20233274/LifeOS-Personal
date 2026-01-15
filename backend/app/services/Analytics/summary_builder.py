# backend/app/services/analytics/summary_builder.py

from datetime import timedelta
from sqlalchemy.orm import Session

from app.models.summary import Summary
from app.services.analytics.time import (
    time_distribution,
    productive_minutes
)
from app.services.analytics.criteria import criteria_breakdown
from app.services.analytics.execution import execution_quality
from app.services.analytics.analytics import task_progress
from app.services.analytics.summaries import (
    daily_summary,
    weekly_summary,
    goal_narrative
)
from app.services.analytics.goal import goal_progress


# --------------------------------------------------
# DAILY SUMMARY
# --------------------------------------------------

def build_daily_summary(
    db: Session,
    user,
    date
) -> Summary:

    start = date
    end = date

    time_by_category = time_distribution(db, user.user_id, start, end)
    productive = productive_minutes(db, user.user_id, start, end)
    total = sum(time_by_category.values())

    criteria = criteria_breakdown(db, user.user_id, start, end)
    execution = execution_quality(db, user.user_id, start, end)

    metrics = {
        "total_minutes": total,
        "productive_minutes": productive,
        "productivity_ratio": productive / total if total else 0,
        "time_by_category": time_by_category,
        "top_criteria": dict(list(criteria.items())[:5]),
        "task_completion": execution["completion_ratio"]
    }

    narrative = daily_summary(
        user,
        {
            **metrics,
            "peak_category": max(time_by_category, key=time_by_category.get) if time_by_category else None,
            "top_non_productive_category": min(time_by_category, key=time_by_category.get) if time_by_category else None
        }
    )

    summary = Summary(
        user_id=user.user_id,
        summary_type="daily",
        period_start=date,
        period_end=date,
        metrics=metrics,
        narrative=narrative
    )

    db.add(summary)
    db.commit()

    return summary


# --------------------------------------------------
# WEEKLY SUMMARY
# --------------------------------------------------

def build_weekly_summary(
    db: Session,
    user,
    week_start
) -> Summary:

    week_end = week_start + timedelta(days=6)

    this_week = productive_minutes(db, user.user_id, week_start, week_end)

    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(days=1)

    last_week = productive_minutes(
        db,
        user.user_id,
        last_week_start,
        last_week_end
    )

    delta = ((this_week - last_week) / last_week * 100) if last_week else 0

    metrics = {
        "weekly_productive_minutes": this_week,
        "delta_percent": delta
    }

    narrative = weekly_summary(
        user,
        {
            **metrics,
            "top_goals": [],
            "top_habit": None,
            "focus_pattern": "Productivity peaks mid-week"
        }
    )

    summary = Summary(
        user_id=user.user_id,
        summary_type="weekly",
        period_start=week_start,
        period_end=week_end,
        metrics=metrics,
        narrative=narrative
    )

    db.add(summary)
    db.commit()

    return summary


# --------------------------------------------------
# GOAL SUMMARY
# --------------------------------------------------

def build_goal_summary(
    db: Session,
    user,
    goal
) -> Summary:

    progress = goal_progress(goal)

    metrics = {
        "goal_progress": progress,
        "importance_level": goal.importance_level
    }

    narrative = goal_narrative(goal, progress)

    summary = Summary(
        user_id=user.user_id,
        summary_type="goal",
        goal_id=goal.goal_id,
        metrics=metrics,
        narrative=narrative
    )

    db.add(summary)
    db.commit()

    return summary
