from sqlalchemy.orm import Session

from app.services.Executor.base import BaseExecutor
from my_agent.models.action_proposal import ActionProposal
from app.models.subtask import Subtask, SubtaskType


class CreateSubtaskExecutor(BaseExecutor):
    action_type = "create_subtask"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        all_proposals: list[ActionProposal],
    ) -> dict:
        payload = proposal.payload

        # -------------------------------------------------
        # Resolve parent task_id from dependency proposals
        # -------------------------------------------------
        task_id = None

        for parent in all_proposals:
            if (
                parent.proposal_id in (proposal.depends_on or [])
                and parent.action_type == "create_task"
                and parent.execution_result
            ):
                task_id = parent.execution_result.get("task_id")
                break

        if task_id is None:
            # This should never happen if dependency_guard is correct,
            # but we fail fast to avoid corrupt data.
            raise RuntimeError(
                f"Cannot create subtask without executed parent task "
                f"(proposal_id={proposal.proposal_id})"
            )

        # -----------------------------
        # Idempotency check
        # -----------------------------
        existing = (
            db.query(Subtask)
            .filter(
                Subtask.user_id == proposal.user_id,
                Subtask.task_id == task_id,
                Subtask.subtask_name == payload["subtask_name"],
            )
            .first()
        )

        if existing:
            return {
                "status": "success",
                "data": {
                    "subtask_id": existing.subtask_id,
                    "deduplicated": True,
                },
            }

        # -----------------------------
        # Create subtask
        # -----------------------------
        subtask = Subtask(
            user_id=proposal.user_id,
            task_id=task_id,
            subtask_name=payload["subtask_name"],
            subtask_type=SubtaskType(payload["subtask_type"]),
            target_value=payload.get("target_value"),
            current_value=0.0,
            weight=payload.get("weight", 1),
            deadline=payload.get("deadline"),
            order_index=payload["order_index"],
            # NOTE: subtask→subtask dependencies are handled
            # by the rewire executor, not here
            depends_on_subtask_id=None,
        )

        db.add(subtask)
        db.flush()

        return {
            "status": "success",
            "data": {
                "subtask_id": subtask.subtask_id
            },
        }
