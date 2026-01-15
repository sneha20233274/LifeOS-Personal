from datetime import date, timedelta
from app.models.subtask import Subtask, SubtaskType


def compute_task_schedule(
    *,
    subtasks: list[Subtask],
    start_date: date
) -> list[dict]:
    """
    Returns computed schedule (derived).
    Does NOT modify DB.
    """

    schedule = []
    cursor = start_date

    # order matters
    ordered = sorted(subtasks, key=lambda s: s.order_index)

    for s in ordered:
        duration_days = 0

        if s.subtask_type == SubtaskType.duration and s.target_value:
            # assume target_value is in minutes
            duration_days = max(1, int(s.target_value // 60 // 2))  # heuristic

        end_date = cursor + timedelta(days=duration_days)

        schedule.append({
            "subtask_id": s.subtask_id,
            "name": s.subtask_name,
            "start_date": cursor,
            "end_date": end_date,
            "deadline": s.deadline
        })

        cursor = end_date

    return schedule

