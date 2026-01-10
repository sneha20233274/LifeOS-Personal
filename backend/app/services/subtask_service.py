# backend/app/services/subtask_service.py

from sqlalchemy.orm import Session
from app.models.subtask import Subtask, SubtaskType
from app.models.activity import Activity
from app.services.Analytics.core import (
    subtask_completion_percent,
    is_subtask_achieved,
)
from app.services.task_service import recompute_task_completion


# ------------------------------------------------
# APPLY ACTIVITY → SUBTASK (AUTOMATIC PROGRESS)
# ------------------------------------------------

def apply_activity_to_subtask(
    db: Session,
    subtask: Subtask,
    activity: Activity
) -> None:
    """
    Applies activity impact to subtask progress.
    """

    # -------- DEPENDENCY CHECK --------
    if subtask.depends_on and not subtask.depends_on.achieved:
        return

    # -------- TYPE-BASED UPDATE --------
    if subtask.subtask_type == SubtaskType.checkbox:
        subtask.achieved = True

    elif subtask.subtask_type == SubtaskType.duration:
        subtask.current_value += activity.duration_minutes or 0

    elif subtask.subtask_type == SubtaskType.count:
        subtask.current_value += 1

    elif subtask.subtask_type == SubtaskType.score:
        if activity.focus_score is not None:
            subtask.current_value = max(
                subtask.current_value,
                activity.focus_score
            )

    elif subtask.subtask_type == SubtaskType.percentage:
        if activity.focus_score is not None:
            subtask.current_value = min(
                100.0,
                max(subtask.current_value, activity.focus_score)
            )

    # -------- ACHIEVEMENT DERIVED --------
    subtask.achieved = is_subtask_achieved(subtask)

    db.commit()
    db.refresh(subtask)

    recompute_task_completion(db, subtask.task_id)


# ------------------------------------------------
# MANUAL SUBTASK UPDATE (USER ACTION)
# ------------------------------------------------

def update_subtask_progress(
    db: Session,
    subtask: Subtask,
    *,
    increment: float | None = None,
    mark_done: bool | None = None
) -> Subtask:
    """
    Manual progress update.
    """

    # -------- DEPENDENCY CHECK --------
    if subtask.depends_on and not subtask.depends_on.achieved:
        raise ValueError("Dependency subtask not completed")

    # -------- TYPE-BASED LOGIC --------
    if subtask.subtask_type == SubtaskType.checkbox:
        if mark_done:
            subtask.achieved = True

    else:
        if increment is None:
            raise ValueError("Increment required")

        subtask.current_value += increment

    # -------- ACHIEVEMENT DERIVED --------
    subtask.achieved = is_subtask_achieved(subtask)

    db.commit()
    db.refresh(subtask)

    # -------- CASCADE UP --------
    recompute_task_completion(db, subtask.task_id)

    return subtask
