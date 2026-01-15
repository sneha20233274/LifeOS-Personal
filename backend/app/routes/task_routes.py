# backend/app/routes/task_routes.py

from fastapi import APIRouter, Depends, HTTPException, status,Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.crud.task_crud import (
    create_task,
    get_task,
    get_tasks_by_goal,
    update_task_fields,
    delete_task
)
from app.utils.oauth2_scheme  import swagger_bearer_auth


router = APIRouter(
   
    tags=["Tasks"],
    dependencies=[Depends(swagger_bearer_auth)]
)


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_route(
    payload: TaskCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Create a task for the currently authenticated user.
    User is extracted from request.state (set by auth middleware).
    """

    # ✅ extract user from request.state
    current_user = request.state.user
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return create_task(db, payload, int(current_user['sub']))



@router.get("/{task_id}", response_model=TaskOut)
def get_task_route(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.get("/goal/{goal_id}", response_model=list[TaskOut])
def get_tasks_for_goal(goal_id: int, db: Session = Depends(get_db)):
    return get_tasks_by_goal(db, goal_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task_route(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    return update_task_fields(
        db,
        task,
        payload.dict(exclude_unset=True)
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    delete_task(db, task)
