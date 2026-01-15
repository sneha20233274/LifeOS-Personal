from fastapi import APIRouter, Depends, Request, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
  
from app.schemas.goal import GoalCreate, GoalUpdate, GoalOut
from app.core.database import get_db

from app.crud.goal_crud import (
    create_goal,
    get_goal,
    get_goals_by_user,
    update_goal,
    delete_goal,
)
from app.utils.oauth2_scheme  import swagger_bearer_auth

router = APIRouter(tags=["goals"], dependencies=[Depends(swagger_bearer_auth)])


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
    # 1️⃣ Debug user payload from middleware
    if not hasattr(request.state, "user") or request.state.user is None:
        print("❌ No user info in request.state.user")
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        print("✅ User payload from request.state.user:", request.state.user)

    # 2️⃣ Debug user_id extraction
    try:
        user_id = int(request.state.user["sub"])
        print("✅ Extracted user_id:", user_id)
    except Exception as e:
        print("❌ Error extracting user_id:", e)
        raise HTTPException(status_code=401, detail="Invalid user info")

    # 3️⃣ Debug incoming goal data
    print("✅ Incoming goal data (goal_in):", goal_in)

    # 4️⃣ Create goal
    try:
        goal_obj = create_goal(db=db, user_id=user_id, obj_in=goal_in)
        print("✅ Goal created successfully:", goal_obj)
    except Exception as e:
        print("❌ Error creating goal:", e)
        raise HTTPException(status_code=500, detail="Failed to create goal")

    return goal_obj


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
