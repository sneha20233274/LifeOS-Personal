from sqlalchemy.orm import Session
from app.services.Executor.base import BaseExecutor, ExecutorResult
from my_agent.models.action_proposal import ActionProposal
from app.models.goal import Goal


class CreateGoalExecutor(BaseExecutor):
    action_type = "create_goal"

    def execute(self, db: Session, proposal: ActionProposal) -> ExecutorResult:
        payload = proposal.payload

        goal = Goal(
            user_id=payload["user_id"],
            goal_name=payload["goal_name"],
            description=payload.get("description"),
            target_date=payload.get("target_date"),
            importance_level=payload.get("importance_level", 1),
            motivations=payload.get("motivations"),
        )

        db.add(goal)
        db.flush()

        return ExecutorResult(
            status="success",
            data={
                "goal_id": goal.goal_id,
                "goal_name": goal.goal_name,
            }
        )
