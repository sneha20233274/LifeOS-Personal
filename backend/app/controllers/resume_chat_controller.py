from sqlalchemy.orm import Session
from langgraph.types import Command

from my_agent.model_gen import chatbot
from my_agent.models.action_proposal import ProposalStatus, ActionProposal
from app.services.Executor.dispatcher import execute_proposals


def resume_chat_controller(
    *,
    request: dict,
    db: Session,
    user_id: int,
):
    """
    Resume an interrupted agent run.

    Steps:
    1. Validate thread ownership
    2. Update proposals in DB based on frontend edits
    3. Execute ONLY incoming + approved proposals
    4. Resume LangGraph
    5. Return final messages
    """

    # -------------------------------------------------
    # STEP 0: PARSE REQUEST
    # -------------------------------------------------
    thread_id = request["thread_id"]
    incoming_proposals = request["proposals"]

    # -------------------------------------------------
    # STEP 1: LOAD & AUTHORIZE PROPOSALS
    # -------------------------------------------------
    db_proposals = (
        db.query(ActionProposal)
        .filter(
            ActionProposal.thread_id == thread_id,
            ActionProposal.user_id == user_id,   # 🔐 authorization
        )
        .all()
    )

    if not db_proposals:
        raise ValueError("Invalid thread_id or access denied")

    db_proposal_map = {p.proposal_id: p for p in db_proposals}

    # -------------------------------------------------
    # STEP 2: APPLY FRONTEND UPDATES
    # -------------------------------------------------
    incoming_ids = set()

    for incoming in incoming_proposals:
        proposal_id = incoming["proposal_id"]
        incoming_ids.add(proposal_id)

        proposal = db_proposal_map.get(proposal_id)
        if not proposal:
            continue

        # Merge payload safely
        proposal.payload = {
            **(proposal.payload or {}),
            **incoming.get("payload", {}),
        }

        # Enum-safe status update
        proposal.status = ProposalStatus[incoming["status"]]

    db.commit()

    # -------------------------------------------------
    # STEP 3: EXECUTE ONLY APPROVED + INCOMING
    # -------------------------------------------------
    executable_proposals = [
        p for p in db_proposals
        if (
            p.proposal_id in incoming_ids
            and p.status == ProposalStatus.APPROVED
        )
    ]

    execution_result = execute_proposals(
        db=db,
        proposals=executable_proposals,
    )

    # -------------------------------------------------
    # STEP 4: RESUME LANGGRAPH
    # -------------------------------------------------
    resumed = chatbot.invoke(
        Command(resume=True),
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    # -------------------------------------------------
    # STEP 5: RESPONSE
    # -------------------------------------------------
    return {
        "status": "RESUMED",
        "executed": execution_result.get("executed", []),
        "messages": resumed.get("messages", []),
    }
