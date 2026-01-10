# app/services/analytics/task.py

from app.services.Analytics.core import subtask_completion_percent


def task_progress(task) -> float:
    """
    Weighted task completion percentage.
    """
    if not task.subtasks:
        return 0.0

    total_weight = sum(s.weight for s in task.subtasks)

    weighted_sum = sum(
        subtask_completion_percent(s) * s.weight
        for s in task.subtasks
    )

    return weighted_sum / total_weight
