from sqlalchemy.orm import Session
from fastapi import HTTPException

from my_agent.models.action_proposal import ActionProposal
from app.services.Executor.goal import CreateGoalExecutor
from app.services.Executor.activity import LogActivityExecutor
from app.services.Executor.subtask import UpdateSubtaskExecutor

EXECUTORS = {
    "create_goal": CreateGoalExecutor(),
    "log_activity": LogActivityExecutor(),
    "update_subtask": UpdateSubtaskExecutor(),
}


def execute_proposal(
    db: Session,
    proposal: ActionProposal,
):
    if proposal.status != "APPROVED":
        raise HTTPException(
            status_code=400,
            detail="Only APPROVED proposals can be executed"
        )

    executor = EXECUTORS.get(proposal.action_type)

    if not executor:
        raise HTTPException(
            status_code=400,
            detail=f"No executor registered for action_type={proposal.action_type}"
        )

    try:
        result = executor.execute(db, proposal)
        proposal.status = "EXECUTED"
        db.commit()
        return result

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
