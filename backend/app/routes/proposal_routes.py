from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from my_agent.models.action_proposal import ActionProposal
from my_agent.models.approval_decision import ApprovalDecision
from my_agent.schemas.proposal import (
    ProposalRead,
    ProposalUpdate,
    ProposalApprove,
    ProposalReject,
)

router = APIRouter(prefix="/proposals", tags=["Proposals"])
@router.get("", response_model=list[ProposalRead])
def list_proposals(
    request: Request,
    run_id: str | None = None,
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id

    query = db.query(ActionProposal)

    if run_id:
        query = query.filter(ActionProposal.run_id == run_id)

    proposals = query.order_by(ActionProposal.created_at.desc()).all()
    return proposals

@router.patch("/{proposal_id}", response_model=ProposalRead)
def update_proposal(
    proposal_id: int,
    data: ProposalUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    proposal = db.query(ActionProposal).get(proposal_id)

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    if proposal.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Only DRAFT proposals can be edited"
        )

    # 🚨 action_type CANNOT be changed
    proposal.payload = data.payload
    proposal.version += 1

    db.commit()
    db.refresh(proposal)

    return proposal

@router.post("/{proposal_id}/approve", response_model=ProposalRead)
def approve_proposal(
    proposal_id: int,
    data: ProposalApprove,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id

    proposal = db.query(ActionProposal).get(proposal_id)

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    if proposal.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Only DRAFT proposals can be approved"
        )

    proposal.status = "APPROVED"

    approval = ApprovalDecision(
        proposal_id=proposal.proposal_id,
        approved_by=user_id,
        decision="APPROVED",
        comment=data.comment,
    )

    db.add(approval)
    db.commit()
    db.refresh(proposal)

    return proposal
@router.post("/{proposal_id}/reject", response_model=ProposalRead)
def reject_proposal(
    proposal_id: int,
    data: ProposalReject,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id

    proposal = db.query(ActionProposal).get(proposal_id)

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    if proposal.status != "DRAFT":
        raise HTTPException(
            status_code=400,
            detail="Only DRAFT proposals can be rejected"
        )

    proposal.status = "REJECTED"

    approval = ApprovalDecision(
        proposal_id=proposal.proposal_id,
        approved_by=user_id,
        decision="REJECTED",
        comment=data.comment,
    )

    db.add(approval)
    db.commit()
    db.refresh(proposal)

    return proposal
