from sqlalchemy.orm import Session
from app.models.subtask import Subtask


def analyze_subtask_deletion(
    db: Session,
    subtask_id: int
) -> dict:
    """
    Analyze impact of deleting a subtask.
    Returns dependents and proposed rewiring.
    """

    target = db.get(Subtask, subtask_id)
    if not target:
        raise ValueError("Subtask not found")

    dependents = (
        db.query(Subtask)
        .filter(Subtask.depends_on_subtask_id == subtask_id)
        .all()
)


    parent_id = target.depends_on_subtask_id

    rewires = [
        {
            "subtask_id": dep.subtask_id,
            "old_depends_on": subtask_id,
            "new_depends_on": parent_id  # may be None
        }
        for dep in dependents
    ]

    return {
        "deleted_subtask": subtask_id,
        "task_id": target.task_id,   # 🔑 needed for schedule computation
        "rewire_plan": rewires
    }
