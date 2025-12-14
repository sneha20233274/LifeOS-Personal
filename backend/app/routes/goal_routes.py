from fastapi import APIRouter, Depends, Request, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
  
from schemas.goal import GoalCreate, GoalUpdate, GoalOut
from core.database import get_db

from crud.goal_crud import (
    create_goal,
    get_goal,
    get_goals_by_user,
    update_goal,
    delete_goal,
)

router = APIRouter(tags=["goals"])


# -------------------------------------------------------------------
# NOTE:
# AuthMiddleware already authenticated the request.
# request.state.user IS GUARANTEED.
# We DO NOT perform authentication checks here.
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# CREATE GOAL
# -------------------------------------------------------------------
@router.post("/", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def api_create_goal(
    request: Request,
    goal_in: GoalCreate,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])
    return create_goal(db=db, user_id=user_id, obj_in=goal_in)


# -------------------------------------------------------------------
# LIST ALL GOALS OF USER
# -------------------------------------------------------------------
@router.get("/", response_model=List[GoalOut])
def api_list_goals(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    user_id = int(request.state.user["sub"])
    return get_goals_by_user(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )


# -------------------------------------------------------------------
# GET SINGLE GOAL
# -------------------------------------------------------------------
@router.get("/{goal_id}", response_model=GoalOut)
def api_get_goal(
    goal_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])

    goal = get_goal(db=db, goal_id=goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return goal


# -------------------------------------------------------------------
# UPDATE GOAL (USER-OWNED FIELDS ONLY)
# -------------------------------------------------------------------
@router.put("/{goal_id}", response_model=GoalOut)
def api_update_goal(
    goal_id: int,
    goal_in: GoalUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])

    goal = get_goal(db=db, goal_id=goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # percent_completion is NOT editable here (enforced by schema + CRUD)
    return update_goal(db=db, goal_id=goal_id, obj_in=goal_in)


# -------------------------------------------------------------------
# DELETE GOAL
# -------------------------------------------------------------------
@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_goal(
    goal_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = int(request.state.user["sub"])

    goal = get_goal(db=db, goal_id=goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    delete_goal(db=db, goal_id=goal_id)
    return None
