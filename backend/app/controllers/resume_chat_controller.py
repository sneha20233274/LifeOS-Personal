from sqlalchemy.orm import Session
from langgraph.types import Command

from my_agent.model_gen import chatbot
from my_agent.models.action_proposal import ProposalStatus, ActionProposal
from app.services.Executor.dispatcher import execute_proposals


def resume_chat_controller(request: dict, db: Session):
    """
    Resume an interrupted agent run.

    Steps:
    1. Update proposals in DB based on frontend edits
    2. Execute ONLY incoming + approved proposals
    3. Resume LangGraph
    4. Return final messages
    """

    # -------------------------------------------------
    # STEP 0: PARSE REQUEST
    # -------------------------------------------------
    body = request
    thread_id = body["thread_id"]
    incoming_proposals = body["proposals"]

    # -------------------------------------------------
    # STEP 1: LOAD ALL PROPOSALS FOR THREAD (ORM)
    # -------------------------------------------------
    db_proposals = (
        db.query(ActionProposal)
        .filter(ActionProposal.thread_id == thread_id)
        .all()
    )

    # Map: proposal_id -> ORM object
    db_proposal_map = {p.proposal_id: p for p in db_proposals}

    # -------------------------------------------------
    # STEP 2: UPDATE DB USING FRONTEND STATE
    # -------------------------------------------------
    print("\n=== APPLYING FRONTEND UPDATES ===")

    incoming_ids = set()

    for incoming in incoming_proposals:
        proposal_id = incoming["proposal_id"]
        incoming_ids.add(proposal_id)

        proposal = db_proposal_map.get(proposal_id)
        if not proposal:
            print(f"⚠️ Proposal {proposal_id} not found in DB")
            continue

        print(
            f"Updating proposal_id={proposal_id} | "
            f"STATUS: {proposal.status} → {incoming['status']}"
        )

        # Merge payload safely
        proposal.payload = {
            **(proposal.payload or {}),
            **incoming.get("payload", {})
        }

        # Update status (enum-safe)
        proposal.status = ProposalStatus[incoming["status"].upper()]

    db.commit()

    # Refresh ORM objects to guarantee DB truth
    for p in db_proposals:
        db.refresh(p)

    print("\n=== AFTER DB COMMIT ===")
    for p in db_proposals:
        print(
            f"proposal_id={p.proposal_id}, "
            f"status={p.status}, "
            f"payload={p.payload}"
        )

    target_db_proposals = [
        p for p in db_proposals
        if p.proposal_id in incoming_ids
    ]

   

    execution_result = execute_proposals(
        db=db,
        proposals=target_db_proposals  # ✅ ORM OBJECTS ONLY
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
    # STEP 5: RETURN FINAL RESPONSE
    # -------------------------------------------------
    return {
        "status": "RESUMED",
        "executed": execution_result.get("executed", []),
        "messages": resumed.get("messages", []),
    }
