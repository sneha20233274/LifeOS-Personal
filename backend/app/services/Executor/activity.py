from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.services.Executor.base import BaseExecutor, ExecutorResult
from my_agent.models.action_proposal import ActionProposal
from app.models.activity import Activity
from app.services.subtask_service import apply_activity_to_subtask


class LogActivityExecutor(BaseExecutor):
    action_type = "log_activity"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal
    ) -> ExecutorResult:

        payload = proposal.payload

        activity = Activity(
            user_id=payload["user_id"],
            activity_name=payload["activity_name"],
            activity_description=payload.get("activity_description"),
            start_ts=payload.get("start_ts") or datetime.now(timezone.utc),
            end_ts=payload.get("end_ts"),
            duration_minutes=payload["duration_minutes"],
            summary_category=payload["summary_category"],
            subtask_id=payload.get("subtask_id"),
            focus_score=payload.get("focus_score"),
            source="executor",
        )

        db.add(activity)
        db.flush()  # get activity_id

        # 🔁 apply subtask progress if linked
        if activity.subtask_id:
            apply_activity_to_subtask(
                db=db,
                subtask=activity.subtask,
                activity=activity
            )

        return ExecutorResult(
            status="success",
            data={
                "activity_id": activity.activity_id,
                "duration_minutes": activity.duration_minutes,
                "summary_category": activity.summary_category,
            }
        )
