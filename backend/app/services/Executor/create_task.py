from sqlalchemy.orm import Session

from app.services.Executor.base import BaseExecutor
from my_agent.models.action_proposal import ActionProposal
from app.models.task import Task


class CreateTaskExecutor(BaseExecutor):
    action_type = "create_task"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        all_proposals: list[ActionProposal],
    ) -> dict:
        payload = proposal.payload

        # -------------------------------------------------
        # Resolve optional goal_id from dependency proposals
        # -------------------------------------------------
        goal_id = None

        for parent in all_proposals:
            if (
                parent.proposal_id in (proposal.depends_on or [])
                and parent.action_type == "create_goal"
                and parent.execution_result
            ):
                goal_id = parent.execution_result.get("goal_id")
                break

        # -----------------------------
        # Idempotency check
        # -----------------------------
        existing = (
            db.query(Task)
            .filter(
                Task.user_id == proposal.user_id,
                Task.task_name == payload["task_name"],
                Task.goal_id == goal_id,   # may be None
            )
            .first()
        )

        if existing:
            return {
                "status": "success",
                "data": {
                    "task_id": existing.task_id,
                    "deduplicated": True
                }
            }

        # -----------------------------
        # Create task
        # -----------------------------
        task = Task(
            user_id=proposal.user_id,
            goal_id=goal_id,   # ✅ optional
            task_name=payload["task_name"],
            description=payload.get("description"),
            difficulty=payload.get("difficulty", 1),
        )

        db.add(task)
        db.flush()  # get task_id

        return {
            "status": "success",
            "data": {
                "task_id": task.task_id
            }
        }
