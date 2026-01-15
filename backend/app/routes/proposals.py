from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from my_agent.models.action_proposal import ActionProposal, ProposalStatus

router = APIRouter(prefix="/proposals", tags=["Proposals"])


@router.get("/pending")
def get_pending_proposals(
    thread_id: str,
    user_id: int,  # injected via auth middleware
    db: Session = Depends(get_db)
):
    return (
        db.query(ActionProposal)
        .filter(
            ActionProposal.thread_id == thread_id,
            ActionProposal.user_id == user_id,
            ActionProposal.status == ProposalStatus.PENDING
        )
        .all()
    )

@router.post("/{proposal_id}/approve")
def approve_proposal(
    proposal_id: int,
    payload: dict | None = None,
    db: Session = Depends(get_db),
):
    proposal = db.query(ActionProposal).get(proposal_id)

    if payload is not None:
        proposal.payload = payload  # human edits JSON

    proposal.status = ProposalStatus.APPROVED
    db.commit()

    return {"status": "approved"}
