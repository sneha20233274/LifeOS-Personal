# backend/app/services/task_completion.py

from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.task import Task
from app.models.subtask import Subtask
from app.services.goal_service import recompute_goal_completion


def recompute_task_completion(db: Session, task_id: int) -> None:
    """
    Recomputes task completion based on weighted subtasks
    and then triggers goal completion recomputation.

    Task completion formula:
    Σ(subtask.weight × achieved) / Σ(subtask.weight) × 100
    """

    # 1️⃣ Fetch task
    task = (
        db.query(Task)
        .filter(Task.task_id == task_id)
        .first()
    )
    if not task:
        return

    # 2️⃣ Enforce TASK dependency
    # If this task depends on another task that is not achieved,
    # this task cannot progress
    if task.depends_on and not task.depends_on.achieved:
        task.percent_completion = 0.0
        task.achieved = False
        db.commit()

        # Still recompute goal to reflect dependency lock
        recompute_goal_completion(db, task.goal_id)
        return

    # 3️⃣ Aggregate weighted subtask completion
    weighted_done, weight_sum = (
        db.query(
            func.sum(
                Subtask.weight *
                case((Subtask.achieved == True, 1), else_=0)
            ),
            func.sum(Subtask.weight)
        )
        .filter(Subtask.task_id == task_id)
        .first()
    )

    # 4️⃣ Compute percent completion
    if weight_sum and weight_sum > 0:
        task.percent_completion = round(
            (weighted_done / weight_sum) * 100,
            2
        )
    else:
        task.percent_completion = 0.0

    # 5️⃣ Auto-achieve task (deterministic rule)
    task.achieved = task.percent_completion >= 95.0

    # 6️⃣ Persist task changes
    db.commit()

    # 7️⃣ Trigger GOAL recomputation
    recompute_goal_completion(db, task.goal_id)
