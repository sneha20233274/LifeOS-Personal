from sqlalchemy.orm import Session
from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from my_agent.model_gen import chatbot
from langchain_core.messages import HumanMessage


def run_chat(request: dict, db: Session, user_id: int):
    prompt = request["prompt"]
    thread_id = request.get("thread_id")

    if not thread_id:
        raise ValueError("thread_id is required")

    config = {"configurable": {"thread_id": thread_id}}

    result = chatbot.invoke(
        {
            "messages": [HumanMessage(content=prompt)],
            "iteration": 0,
            "max_iterations": 5,
        },
        config=config,
    )

    if "__interrupt__" in result:
        proposals_data = result.get("proposals", [])

        saved_proposals = save_proposals(
            db=db,
            thread_id=thread_id,
            user_id=user_id,
            proposals=proposals_data,
        )

        apply_dependencies(db, saved_proposals)

        # Serialize DB proposals for frontend
        serializable_proposals = []
        for p in saved_proposals:
            serializable_proposals.append(
                {
                    "proposal_id": p.proposal_id,      # ✅ REAL DB ID
                    "action_type": p.action_type,
                    "status": p.status.name,            # enum → string
                    "payload": p.payload or {},
                }
            )

        return {
            "status": "WAITING_FOR_APPROVAL",
            "thread_id": thread_id,
            "proposals": serializable_proposals,
        }

    return {
        "status": "COMPLETED",
        "thread_id": thread_id,
    }
