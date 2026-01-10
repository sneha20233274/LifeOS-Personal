from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from my_agent.models.action_proposal import ActionProposal
from app.services.Executor.dispatcher import execute_proposal

router = APIRouter(prefix="/executor", tags=["Executor"])


@router.post("/{proposal_id}/execute")
def execute_approved_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
):
    proposal = db.query(ActionProposal).get(proposal_id)

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    return execute_proposal(db, proposal)
