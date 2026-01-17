# backend/app/routes/task_routes.py

from fastapi import APIRouter, Depends, HTTPException, status,Request
from sqlalchemy.orm import Session
from typing import List
from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.models import User
from app.crud.task_crud import (
    create_task,
    get_task,
    get_tasks_by_goal,
    update_task_fields,
    delete_task,
    get_tasks_by_user
  

)




router = APIRouter(
   
    tags=["Tasks"],
  
)


@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED
)
def create_task_route(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(
        db=db,
        payload=payload,
        user_id=current_user.user_id
    )





# ✅ ALL TASKS OF USER
@router.get("", response_model=List[TaskOut])
def get_tasks(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.user_id
    return get_tasks_by_user(db=db, user_id=user_id)


# ✅ TASKS FOR A PARTICULAR GOAL
@router.get("/by-goal/{goal_id}", response_model=List[TaskOut])
def get_tasks_for_goal(
    goal_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.user_id
    return get_tasks_by_goal(
        db=db,
        user_id=user_id,
        goal_id=goal_id,
    )

@router.get("/{task_id}", response_model=TaskOut)
def get_task_route(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task




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
