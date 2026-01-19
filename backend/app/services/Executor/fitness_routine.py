from sqlalchemy.orm import Session
from datetime import datetime
from my_agent.chatstate import ChatState
from app.models.fitness import UserFitnessRoutinesDB


def fitness_routine_executor_node(
    state: ChatState,
    db: Session
) -> ChatState:
    """
    Appends a new weekly fitness routine.
    The last routine in the list is always the current one.
    """

    weekly_routine = state.get("weekly_routine")
    user_id = state.get("user_id")

    if not weekly_routine:
        raise ValueError("weekly_routine missing")

    if not user_id:
        raise ValueError("user_id missing")

    record = (
        db.query(UserFitnessRoutinesDB)
        .filter(UserFitnessRoutinesDB.user_id == user_id)
        .one_or_none()
    )

    if record is None:
        # First routine ever
        record = UserFitnessRoutinesDB(
            user_id=user_id,
            routines=[weekly_routine]
        )
        db.add(record)
    else:
        # Append new routine
        routines = record.routines
        routines.append(weekly_routine)
        record.routines = routines

    db.commit()

    return {
        **state,
        "execution_result": "fitness_routine_appended"
    }
