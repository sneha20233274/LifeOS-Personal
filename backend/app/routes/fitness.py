from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.weekly_fitness_routine import WeeklyFitnessRoutineDB, RoutineStatus
from app.schemas.weekly_fitness_routine import WeeklyFitnessRoutineResponse

router = APIRouter(tags=["Fitness"])
@router.get(
    "/weekly-routine",
    response_model=WeeklyFitnessRoutineResponse
)
def get_weekly_fitness_routine(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    Fetch user's weekly fitness routine.

    Priority:
    1️⃣ Approved routine
    2️⃣ Latest draft (fallback)
    """

    # 1️⃣ Try approved routine first
    routine = (
        db.query(WeeklyFitnessRoutineDB)
        .filter(
            WeeklyFitnessRoutineDB.user_id == user_id,
            WeeklyFitnessRoutineDB.status == RoutineStatus.approved,
        )
        .order_by(WeeklyFitnessRoutineDB.created_at.desc())
        .first()
    )

    # 2️⃣ Fallback to latest draft
    if not routine:
        routine = (
            db.query(WeeklyFitnessRoutineDB)
            .filter(WeeklyFitnessRoutineDB.user_id == user_id)
            .order_by(WeeklyFitnessRoutineDB.created_at.desc())
            .first()
        )

    if not routine:
        raise HTTPException(
            status_code=404,
            detail="No weekly fitness routine found",
        )

    return routine
