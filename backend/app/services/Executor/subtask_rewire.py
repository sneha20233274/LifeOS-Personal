from sqlalchemy.orm import Session

from app.services.Executor.base import BaseExecutor
from my_agent.models.action_proposal import ActionProposal
from app.models.subtask import Subtask


class RewireSubtaskDependencyExecutor(BaseExecutor):
    action_type = "rewire_subtask_dependency"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        all_proposals: list[ActionProposal],
    ) -> dict:
        payload = proposal.payload
        subtask_id = payload["subtask_id"]
        new_depends_on = payload.get("depends_on_subtask_id")

        subtask = db.get(Subtask, subtask_id)

        # -----------------------------
        # Idempotency / safety
        # -----------------------------
        if not subtask:
            return {
                "status": "success",
                "data": {
                    "subtask_id": subtask_id,
                    "deduplicated": True,
                    "reason": "subtask_not_found",
                },
            }

        # -----------------------------
        # Idempotency: already rewired
        # -----------------------------
        if subtask.depends_on_subtask_id == new_depends_on:
            return {
                "status": "success",
                "data": {
                    "subtask_id": subtask.subtask_id,
                    "depends_on": subtask.depends_on_subtask_id,
                    "deduplicated": True,
                },
            }

        # -----------------------------
        # Apply rewiring
        # -----------------------------
        subtask.depends_on_subtask_id = new_depends_on
        db.flush()

        return {
            "status": "success",
            "data": {
                "subtask_id": subtask.subtask_id,
                "depends_on": subtask.depends_on_subtask_id,
            },
        }
