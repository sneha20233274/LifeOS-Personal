# backend/app/crud/task_crud.py

from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate
from fastapi import APIRouter, Depends, Request, HTTPException, status, Query
from app.models.goal import Goal


def create_task(
    db: Session,
    payload: TaskCreate,
    user_id: int,
) -> Task:

    # 1️⃣ Validate goal ONLY if provided
    if payload.goal_id is not None:
        goal = (
            db.query(Goal)
            .filter(
                Goal.goal_id == payload.goal_id,
                Goal.user_id == user_id
            )
            .first()
        )
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )

    # 2️⃣ Validate dependency ONLY if provided
    if payload.depends_on_task_id is not None:
        parent_task = (
            db.query(Task)
            .filter(
                Task.task_id == payload.depends_on_task_id,
                Task.user_id == user_id
            )
            .first()
        )
        if not parent_task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dependency task not found"
            )

    # 3️⃣ Create task
    task = Task(
        user_id=user_id,
        task_name=payload.task_name,
        description=payload.description,
        goal_id=payload.goal_id,
        difficulty=payload.difficulty,
        depends_on_task_id=payload.depends_on_task_id,
        percent_completion=0,
        achieved=False,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task



def get_tasks_by_user(db: Session, user_id: int):
    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )

def get_task(db: Session, task_id: int) -> Task | None:
    return (
        db.query(Task)
        .filter(Task.task_id == task_id)
        .first()
    )


def get_tasks_by_goal(db: Session,user_id: int, goal_id: int):
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
