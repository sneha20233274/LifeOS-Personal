from sqlalchemy.orm import Session
from app.services.Executor.base import BaseExecutor
from my_agent.models.action_proposal import ActionProposal
from app.models.goal import Goal


class CreateGoalExecutor(BaseExecutor):
    action_type = "create_goal"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        all_proposals: list[ActionProposal],
    ) -> dict:
        payload = proposal.payload

        # -----------------------------
        # Optional idempotency
        # -----------------------------
        existing = (
            db.query(Goal)
            .filter(
                Goal.user_id == proposal.user_id,
                Goal.goal_name == payload["goal_name"],
            )
            .first()
        )

        if existing:
            return {
                "status": "success",
                "data": {
                    "goal_id": existing.goal_id,
                    "deduplicated": True,
                }
            }

        # -----------------------------
        # Create goal
        # -----------------------------
        goal = Goal(
            user_id=proposal.user_id,
            goal_name=payload["goal_name"],
            description=payload.get("description"),
            target_date=payload.get("target_date"),
            importance_level=payload.get("importance_level", 1),
            motivations=payload.get("motivations"),
        )

        db.add(goal)
        db.flush()  # populate goal_id

        return {
            "status": "success",
            "data": {
                "goal_id": goal.goal_id
            }
        }
