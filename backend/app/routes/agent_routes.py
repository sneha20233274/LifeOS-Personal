from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from my_agent.run_agent import run_agent
from my_agent.models.action_proposal import ActionProposal, ProposalStatus
from app.services.Executor.dispatcher import execute_proposals
from my_agent.model_gen import chatbot
router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/run")
def run_agent_route(
    user_input: str,
    user_id: int,  # injected by auth middleware later
    db: Session = Depends(get_db)
):
    """
    Starts an agent run.
    May pause for HITL approval.
    """
    result = run_agent(
        user_input=user_input,
        user_id=user_id,
        db=db
    )

    return result

@router.post("/{thread_id}/resume")
def resume_agent(
    thread_id: str,
    user_id: int,  # injected via auth middleware
    db: Session = Depends(get_db),
):
    proposals = (
        db.query(ActionProposal)
        .filter(
            ActionProposal.thread_id == thread_id,
            ActionProposal.user_id == user_id,
            ActionProposal.status == ProposalStatus.APPROVED
        )
        .all()
    )

    if not proposals:
        raise HTTPException(400, "No approved proposals")

    # 🔥 EXECUTE
    execution_result = execute_proposals(
        db=db,
        proposals=proposals
    )

    # 🔁 RESUME LANGGRAPH
    chatbot.invoke(
        {
            "execution_result": execution_result
        },
        config={"thread_id": thread_id}
    )

    return {
        "status": "resumed",
        "execution_result": execution_result
    }

