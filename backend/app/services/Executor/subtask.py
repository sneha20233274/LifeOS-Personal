from sqlalchemy.orm import Session
from app.services.Executor.base import BaseExecutor, ExecutorResult
from my_agent.models.action_proposal import ActionProposal
from app.services.subtask_service import update_subtask_progress


class UpdateSubtaskExecutor(BaseExecutor):
    action_type = "update_subtask"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal
    ) -> ExecutorResult:
        payload = proposal.payload

        subtask = update_subtask_progress(
            db=db,
            subtask_id=payload["subtask_id"],
            increment=payload.get("increment"),
            mark_done=payload.get("mark_done"),
        )

        return ExecutorResult(
            status="success",
            data={
                "subtask_id": subtask.subtask_id,
                "achieved": subtask.achieved,
                "current_value": subtask.current_value,
            }
        )
