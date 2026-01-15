from fastapi import APIRouter, Depends, Request, HTTPException, status, Query
from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityOut
from app.core.database import get_db

from app.crud.activity_crud import (
    create_activity,
    get_activity,
    get_activities_by_user,
    get_user_activities_in_period,
    get_subtask_activities_by_duration,
    update_activity,
    delete_activity,
    get_time_spent_by_summary_category,
    get_time_spent_by_criteria,
)
from app.utils.oauth2_scheme  import swagger_bearer_auth
router = APIRouter(tags=["activities"], dependencies=[Depends(swagger_bearer_auth)])


# -------------------------------------------------------------------
# NOTE:
# request.state.user IS GUARANTEED by AuthMiddleware
# Do NOT do auth checks here
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# CRUD ROUTES
# -------------------------------------------------------------------

@router.post("/", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def api_create_activity(
    request: Request,
    activity_in: ActivityCreate,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])
    return create_activity(db=db, user_id=user_id, obj_in=activity_in)


@router.get("/", response_model=List[ActivityOut])
def api_list_activities(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    user_id = int(request.state.user["sub"])
    return get_activities_by_user(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{activity_id}", response_model=ActivityOut)
def api_get_activity(
    activity_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])

    activity = get_activity(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return activity


@router.put("/{activity_id}", response_model=ActivityOut)
def api_update_activity(
    activity_id: int,
    activity_in: ActivityUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])

    activity = get_activity(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return update_activity(db=db, activity_id=activity_id, obj_in=activity_in)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_activity(
    activity_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])

    activity = get_activity(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    delete_activity(db=db, activity_id=activity_id)
    return None


# -------------------------------------------------------------------
# ANALYTICS / QUERY ROUTES
# -------------------------------------------------------------------

@router.get("/period", response_model=List[ActivityOut])
def api_get_activities_in_period(
    request: Request,
    start: datetime = Query(..., description="ISO start datetime (inclusive)"),
    end: datetime = Query(..., description="ISO end datetime (inclusive)"),
    limit: int = Query(500, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Returns up to `limit` most recent activities between start and end.
    Used for analytics & AI context.
    """
    user_id = int(request.state.user["sub"])

    if start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")

    return get_user_activities_in_period(
        db=db,
        user_id=user_id,
        start_date=start,
        end_date=end,
        limit=limit,
    )


@router.get("/subtask/{subtask_id}", response_model=List[ActivityOut])
def api_get_subtask_activities(
    subtask_id: int,
    request: Request,
    min_duration_minutes: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Returns activities for a subtask filtered by minimum duration.
    Ownership enforced.
    """
    user_id = int(request.state.user["sub"])

    activities = get_subtask_activities_by_duration(
        db=db,
        subtask_id=subtask_id,
        min_duration_minutes=min_duration_minutes,
    )

    # enforce ownership
    return [a for a in activities if a.user_id == user_id]


@router.get("/time/summary", response_model=Dict[str, int])
def api_time_spent_by_summary(
    request: Request,
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db),
):
    """
    Time spent grouped by summary_category.
    PRIMARY input for AI feedback.
    """
    user_id = int(request.state.user["sub"])

    if start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")

    data = get_time_spent_by_summary_category(
        db=db,
        user_id=user_id,
        start_date=start,
        end_date=end,
    )

    return {str(k): int(v) for k, v in data.items()}


@router.get("/time/criteria", response_model=Dict[str, int])
def api_time_spent_by_criteria(
    request: Request,
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db),
):
    """
    Time spent grouped by semantic criteria (tags).
    Used for drill-downs & AI reasoning.
    """
    user_id = int(request.state.user["sub"])

    if start > end:
        raise HTTPException(status_code=400, detail="start must be <= end")

    data = get_time_spent_by_criteria(
        db=db,
        user_id=user_id,
        start_date=start,
        end_date=end,
    )

    return {str(k): int(v) for k, v in data.items()}
