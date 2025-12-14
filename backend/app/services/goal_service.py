from sqlalchemy import func
from models.task import Task
from crud.goal_crud import get_goal
from sqlalchemy.orm import Session

def recompute_goal_completion(db: Session, goal_id: int) -> None:
    """
    Recomputes goal completion as:
    Σ(task.difficulty × task.percent_completion) / Σ(task.difficulty)
    """

    weighted_sum, difficulty_sum = (
        db.query(
            func.sum(Task.difficulty * Task.percent_completion),
            func.sum(Task.difficulty),
        )
        .filter(Task.goal_id == goal_id)
        .first()
    )

    goal = get_goal(db, goal_id)
    if not goal:
        return

    if difficulty_sum and difficulty_sum > 0:
        goal.percent_completion = round(weighted_sum / difficulty_sum, 2)
    else:
        goal.percent_completion = 0.0

    db.commit()
