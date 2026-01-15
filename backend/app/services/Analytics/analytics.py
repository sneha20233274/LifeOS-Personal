# backend/app/services/analytics/analytics.py

from app.services.Analytics.core import subtask_completion_percent


def task_progress(task) -> float:
    """
    Weighted task completion percentage.
    """
    if not task.subtasks:
        return 0.0

    total_weight = sum(s.weight for s in task.subtasks)

    weighted_completion = sum(
        subtask_completion_percent(s) * s.weight
        for s in task.subtasks
    )

    return weighted_completion / total_weight


def goal_progress(goal) -> float:
    """
    Weighted goal completion percentage.
    """
    if not goal.tasks:
        return 0.0

    total_difficulty = sum(t.difficulty for t in goal.tasks)

    weighted = sum(
        t.percent_completion * t.difficulty
        for t in goal.tasks
    )

    return weighted / total_difficulty
