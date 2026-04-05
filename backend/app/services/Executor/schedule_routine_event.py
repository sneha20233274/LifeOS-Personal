from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.routine_event import RoutineEvent
from my_agent.models.action_proposal import ActionProposal


class ScheduleRoutineEventExecutor:
    """
    Executor for scheduling routine events.
    Action type: schedule_routine_event
    """

    def execute(
        self,
        db: Session,
        proposal: ActionProposal,
        all_proposals: list[ActionProposal],
    ):
        payload = proposal.payload

        start_time = payload["start_time"]
        end_time = payload["end_time"]

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)

        if end_time <= start_time:
            raise HTTPException(
                status_code=400,
                detail="end_time must be after start_time"
            )

        event = RoutineEvent(
            user_id=proposal.user_id,
            title=payload["title"],
            description=payload.get("description"),
            start_time=start_time,
            end_time=end_time,
            is_all_day=payload.get("is_all_day", False),
            category=payload.get("category", "General"),
            priority=payload.get("priority", "Medium"),
            location_or_link=payload.get("location_or_link"),
            source=payload.get("source", "ai"),
        )

        db.add(event)
        db.flush()  # get event.id without committing

        return {
            "data": {
                "routine_event_id": event.id,
            }
        }
# "data": {
#                 "routine_event_id": event.id,
#                 "temp_event_key": payload.get("temp_event_key"),
#                 "start_time": event.start_time.isoformat(),
#                 "end_time": event.end_time.isoformat(),
#                 "title": event.title,
#             }