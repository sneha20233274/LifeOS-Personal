# backend/app/services/subtask_service.py

from sqlalchemy.orm import Session
from app.models.subtask import Subtask
from app.models.activity import Activity


def apply_activity_to_subtask(
    db: Session,
    subtask: Subtask,
    activity: Activity
) -> None:
    """
    Applies activity progress to subtask.
    Uses existing Activity fields.
    """

    # --- dependency check ---
    if subtask.depends_on and not subtask.depends_on.achieved:
        return

    if subtask.subtask_type == "checkbox": 
        # here mai assume krri hu k ek hi activity ise complete krderi hai ...
        subtask.achieved = True

    elif subtask.subtask_type == "duration":
        subtask.current_value += activity.duration_minutes or 0

    elif subtask.subtask_type == "count":
        subtask.current_value += 1

    elif subtask.subtask_type == "score":
        if activity.focus_score is not None:
            subtask.current_value = max(
                subtask.current_value,
                activity.focus_score
            )

    # --- threshold auto completion ---
    if subtask.target_value is not None:
        if subtask.current_value >= subtask.target_value:
            subtask.achieved = True

    db.commit()


from app.services.task_service import recompute_task_completion



def update_subtask_progress(
    db: Session,
    subtask: Subtask,
    *,
    increment: float | None = None,
    mark_done: bool | None = None
) -> Subtask:
    """
    Updates subtask progress based on its type
    and triggers task & goal recomputation.
    """

    # -------- DEPENDENCY CHECK --------
    if subtask.depends_on and not subtask.depends_on.achieved:
        raise ValueError("Dependency subtask not completed")

    # -------- TYPE-BASED LOGIC --------
    if subtask.subtask_type.value == "checkbox":
        if mark_done is True:
            subtask.achieved = True

    else:
        if increment is None:
            raise ValueError("Increment value required")

        subtask.current_value += increment

        if subtask.target_value is not None:
            if subtask.current_value >= subtask.target_value:
                subtask.achieved = True

    db.commit()
    db.refresh(subtask)

    # -------- CASCADE UP --------
    print(subtask.achieved)
    recompute_task_completion(db, subtask.task_id)

    return subtask
