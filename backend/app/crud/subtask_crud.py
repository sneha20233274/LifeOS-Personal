# backend/app/crud/subtask_crud.py

from sqlalchemy.orm import Session
from app.models.subtask import Subtask
from app.schemas.subtask import SubtaskCreate


def create_subtask(
    db: Session,
    payload: SubtaskCreate,
    user_id: int
) -> Subtask:
    subtask = Subtask(
        user_id=user_id,
        **payload.dict()
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


def get_subtasks_by_task(db: Session, task_id: int):
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
