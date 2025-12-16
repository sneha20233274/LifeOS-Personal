# backend/app/crud/task_crud.py

from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(db: Session, payload: TaskCreate, user_id: int) -> Task:
    task = Task(
        user_id=user_id,
        **payload.dict()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task | None:
    return (
        db.query(Task)
        .filter(Task.task_id == task_id)
        .first()
    )


def get_tasks_by_goal(db: Session, goal_id: int):
    return (
        db.query(Task)
        .filter(Task.goal_id == goal_id)
        .all()
    )


def update_task_fields(db: Session, task: Task, updates: dict) -> Task:
    for key, value in updates.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
