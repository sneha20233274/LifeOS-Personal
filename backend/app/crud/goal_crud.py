# backend/app/crud/goal.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


def create_goal(db: Session, user_id: int, obj_in: GoalCreate) -> Goal:
    """
    Creates a new goal.
    percent_completion is system-managed and always starts at 0.0
    """

    db_obj = Goal(
        user_id=user_id,
        goal_name=obj_in.goal_name,
        description=obj_in.description,
        target_date=obj_in.target_date,
        importance_level=obj_in.importance_level,
        motivations=obj_in.motivations,
        percent_completion=0.0,   # 🔒 system default
    )
    print("CREATED GOAL:", db_obj)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_goal(db: Session, goal_id: int) -> Optional[Goal]:
    return (
        db.query(Goal)
        .filter(Goal.goal_id == goal_id)
        .first()
    )


def get_goals_by_user(
    db: Session,
    user_id: int,
) -> List[Goal]:
    return (
        db.query(Goal)
        .filter(Goal.user_id == user_id)
        .order_by(Goal.created_at.desc())
        .all()
    )

def update_goal(
    db: Session,
    goal_id: int,
    obj_in: GoalUpdate
) -> Optional[Goal]:
    """
    Updates goal metadata.
    percent_completion is NOT editable here.
    """

    db_obj = get_goal(db, goal_id)
    if not db_obj:
        return None

    update_data = obj_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj
def delete_goal(db: Session, goal_id: int) -> bool:
  db.query(Goal).filter(Goal.goal_id == goal_id).delete()
  db.commit()
