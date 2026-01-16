from sqlalchemy.orm import Session
from app.services.Executor.base import BaseExecutor, ExecutorResult
from my_agent.models.action_proposal import ActionProposal
from app.models.activity import Activity
from app.models.criteria import Criteria
from app.services.subtask_service import apply_activity_to_subtask


class LogActivityExecutor(BaseExecutor):
    action_type = "log_activity"

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        proposals: list[ActionProposal],
    ) -> ExecutorResult:

        payload = proposal.payload

        activity = Activity(
            user_id=proposal.user_id,  # ✅ FIX HERE
            activity_name=payload["activity_name"],
            activity_description=payload.get("activity_description"),
            start_ts=payload.get("start_ts"),
            end_ts=payload.get("end_ts"),
            duration_minutes=payload["duration_minutes"],
            summary_category=payload["summary_category"],
            subtask_id=payload.get("subtask_id"),
            source="executor",
        )

        db.add(activity)
        db.flush()  # get activity_id

        # ✅ attach criteria (M2M)
        criteria_ids = payload.get("criteria_ids", [])
        if criteria_ids:
            criteria_rows = (
                db.query(Criteria)
                .filter(Criteria.criteria_id.in_(criteria_ids))
                .all()
            )
            activity.criteria.extend(criteria_rows)

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
            },
        )
