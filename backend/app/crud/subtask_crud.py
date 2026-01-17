# backend/app/crud/subtask_crud.py

from sqlalchemy.orm import Session
from app.models.subtask import Subtask
from app.schemas.subtask import SubtaskCreate
from app.models import Task
from app.schemas.subtask import SubtaskCreate, SubtaskType
from fastapi import APIRouter, Depends, Request, HTTPException, status, Query


def create_subtask(
    db: Session,
    payload: SubtaskCreate,
    user_id: int
) -> Subtask:
    # 1️⃣ Validate parent task exists & belongs to user
    task = (
        db.query(Task)
        .filter(
            Task.task_id == payload.task_id,
            Task.user_id == user_id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # 2️⃣ Validate target_value rules
    if payload.subtask_type != SubtaskType.checkbox and payload.target_value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="target_value is required for this subtask type"
        )

    if payload.subtask_type == SubtaskType.checkbox and payload.target_value is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="checkbox subtask cannot have target_value"
        )

    # 3️⃣ Create subtask (goal_id inferred from task)
    subtask = Subtask(
        user_id=user_id,
        task_id=payload.task_id,
        goal_id=payload.goal_id or task.goal_id,

        subtask_name=payload.subtask_name,
        subtask_type=payload.subtask_type,
        target_value=payload.target_value,
        weight=payload.weight,
        deadline=payload.deadline,
        depends_on_subtask_id=payload.depends_on_subtask_id,

        achieved=False,
        current_value=0,
    )

    db.add(subtask)
    db.commit()
    db.refresh(subtask)

    return subtask



def get_subtask(db: Session, subtask_id: int) -> Subtask | None:
    return (
        db.query(Subtask)
        .filter(Subtask.subtask_id == subtask_id)
        .first()
    )


def get_subtasks_by_task(db: Session,user_id:int, task_id: int):
    return (
        db.query(Subtask)
        .filter(Subtask.task_id == task_id)
        .all()
    )


def update_subtask_fields(
    db: Session,
    subtask: Subtask,
    updates: dict
) -> Subtask:
    for key, value in updates.items():
        setattr(subtask, key, value)
    db.commit()
    db.refresh(subtask)
    return subtask


def delete_subtask(db: Session, subtask: Subtask) -> None:
    db.delete(subtask)
    db.commit()
