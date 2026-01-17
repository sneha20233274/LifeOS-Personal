# backend/app/routes/subtask_routes.py

from fastapi import APIRouter, Depends, HTTPException, status,Request
from sqlalchemy.orm import Session
from typing import List
from app.models import User
from app.core.database import get_db
from app.schemas.subtask import (
    SubtaskCreate,
    SubtaskUpdate,
    SubtaskOut
)
from app.crud.subtask_crud import (
    create_subtask,
    get_subtask,
    get_subtasks_by_task,
    update_subtask_fields,
    delete_subtask
)
from app.core.security import get_current_user



router = APIRouter(
   
    tags=["Subtasks"]
   
)

@router.post(
    "/",
    response_model=SubtaskOut,
    status_code=status.HTTP_201_CREATED
)
def create_subtask_route(
    payload: SubtaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a subtask for the authenticated user.
    """

    return create_subtask(
        db=db,
        payload=payload,
        user_id=current_user.user_id
    )

@router.get("/{subtask_id}", response_model=SubtaskOut)
def get_subtask_route(
    subtask_id: int,
    db: Session = Depends(get_db)
):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask


@router.get("/by-task/{task_id}", response_model=List[SubtaskOut])
def get_subtasks(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.user_id
    return get_subtasks_by_task(
        db=db,
        user_id=user_id,
        task_id=task_id,
    )

@router.patch("/{subtask_id}", response_model=SubtaskOut)
def update_subtask_route(
    subtask_id: int,
    payload: SubtaskUpdate,
    db: Session = Depends(get_db)
):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")

    return update_subtask_fields(
        db,
        subtask,
        payload.dict(exclude_unset=True)
    )


@router.delete("/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subtask_route(
    subtask_id: int,
    db: Session = Depends(get_db)
):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")

    delete_subtask(db, subtask)





from app.services.subtask_service import update_subtask_progress




@router.post("/{subtask_id}/complete", response_model=SubtaskOut)
def complete_checkbox_subtask(
    subtask_id: int,
    db: Session = Depends(get_db)
):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(404, "Subtask not found")

    if subtask.subtask_type.value != "checkbox":
        raise HTTPException(400, "Not a checkbox subtask")

    return update_subtask_progress(
        db,
        subtask,
        mark_done=True
    )


from fastapi import Query

@router.post("/{subtask_id}/progress", response_model=SubtaskOut)
def progress_subtask(
    subtask_id: int,
    increment: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(404, "Subtask not found")

    if subtask.subtask_type.value == "checkbox":
        raise HTTPException(400, "Checkbox subtasks use /complete")

    return update_subtask_progress(
        db,
        subtask,
        increment=increment
    )

from app.services.subtask_service import  update_subtask_progress



@router.patch(
    "/{subtask_id}/progress",
    response_model=SubtaskOut
)
def update_subtask_progress_route(
    subtask_id: int,
    payload: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    subtask = get_subtask(db, subtask_id)
    if not subtask:
        raise HTTPException(404, "Subtask not found")

    return update_subtask_progress(
        db,
        subtask,
        increment=payload.get("increment"),
        mark_done=payload.get("mark_done")
    )


