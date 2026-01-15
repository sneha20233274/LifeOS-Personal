from sqlalchemy.orm import Session

from app.services.Executor.base import BaseExecutor
from my_agent.models.action_proposal import ActionProposal
from app.models.subtask import Subtask


class DeleteSubtaskExecutor(BaseExecutor):
    action_type = "delete_subtask"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        all_proposals: list[ActionProposal],
    ) -> dict:
        payload = proposal.payload
        subtask_id = payload["subtask_id"]

        subtask = db.get(Subtask, subtask_id)

        # -----------------------------
        # Idempotency: already deleted
        # -----------------------------
        if not subtask:
            return {
                "status": "success",
                "data": {
                    "subtask_id": subtask_id,
                    "deduplicated": True,
                },
            }

        # -----------------------------
        # Delete subtask
        # -----------------------------
        db.delete(subtask)
        db.flush()

        return {
            "status": "success",
            "data": {
                "subtask_id": subtask_id
            },
        }
