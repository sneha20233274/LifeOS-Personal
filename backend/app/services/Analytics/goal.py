# app/services/analytics/goal.py
def goal_progress(goal) -> float:
    """
    Weighted goal completion percentage.
    """
    if not goal.tasks:
        return 0.0

    total_difficulty = sum(t.difficulty for t in goal.tasks)

    weighted_sum = sum(
        t.percent_completion * t.difficulty
        for t in goal.tasks
    )

    return weighted_sum / total_difficulty
