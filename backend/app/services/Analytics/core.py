# backend/app/services/analytics/core.py

from app.models.subtask import SubtaskType
from app.models.enums import SummaryCategoryEnum

# -----------------------------
# PRODUCTIVITY RULES
# -----------------------------

PRODUCTIVE_CATEGORIES = {
    SummaryCategoryEnum.work,
    SummaryCategoryEnum.learning,
    SummaryCategoryEnum.exercise,
}


# -----------------------------
# SUBTASK COMPLETION (CANONICAL)
# -----------------------------

def subtask_completion_percent(subtask) -> float:
    """
    Returns exact completion percentage (0–100).
    This is the ONLY place percentage logic lives.
    """

    if subtask.subtask_type == SubtaskType.checkbox:
        return 100.0 if subtask.achieved else 0.0

    if subtask.subtask_type in {
        SubtaskType.count,
        SubtaskType.duration,
        SubtaskType.score,
        SubtaskType.percentage,
    }:
        if not subtask.target_value or subtask.target_value <= 0:
            return 0.0

        return min(
            (subtask.current_value / subtask.target_value) * 100.0,
            100.0
        )

    return 0.0


def is_subtask_achieved(subtask) -> bool:
    return subtask_completion_percent(subtask) >= 100.0
