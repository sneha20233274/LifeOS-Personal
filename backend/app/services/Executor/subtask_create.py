from sqlalchemy.orm import Session

from app.services.Executor.base import BaseExecutor
from my_agent.models.action_proposal import ActionProposal
from app.models.subtask import Subtask, SubtaskType
from app.utils.date_helper import coerce_date

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
        subtask_depends_on = None
        for parent in all_proposals:
            if (
                parent.proposal_id in (proposal.depends_on or [])
                and parent.action_type == "create_task"
                and parent.execution_result
            ):
                task_id = parent.execution_result.get("task_id")
                break
            if( parent.action_type == "create_subtask"
                and parent.execution_result
                and parent.proposal_id in (proposal.depends_on or [])
            ):
                subtask_depends_on = parent.execution_result.get("subtask_id")
        

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
            print(f"[CreateSubtaskExecutor] Deduplicated existing subtask_id={existing.subtask_id}")
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
            deadline= coerce_date(payload.get("deadline")),
        
            # NOTE: subtask→subtask dependencies are handled
            # by the rewire executor, not here
            depends_on_subtask_id=subtask_depends_on,
        )


        db.add(subtask)
        db.flush()
        print(f"[CreateSubtaskExecutor] Created new subtask_id={subtask.subtask_id}")
        return {
            "status": "success",
            "data": {
                "subtask_id": subtask.subtask_id
            },
        }
