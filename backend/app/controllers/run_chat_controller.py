from sqlalchemy.orm import Session
from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from my_agent.model_gen import chatbot
from langchain_core.messages import AIMessage, HumanMessage


def run_chat(request: dict, db: Session, user_id: int):
    prompt = request["prompt"]
    thread_id = request.get("thread_id")

    if not thread_id:
        raise ValueError("thread_id is required")

    config = {
    "configurable": {
        "thread_id": thread_id,
        "user_id": user_id,
        "db": db   # ✅ ADD THIS
    }
}

    result = chatbot.invoke(
        {
            "messages": [HumanMessage(content=prompt)],
            "iteration": 0,
            "max_iterations": 5,
        },
        config=config,
    )

    # -------------------------------
    # HANDLE INTERRUPT (PROPOSALS)
    # -------------------------------
    if "__interrupt__" in result:
        proposals_data = result.get("proposals", [])

        saved_proposals = save_proposals(
            db=db,
            thread_id=thread_id,
            user_id=user_id,
            proposals=proposals_data,
        )

        apply_dependencies(db, saved_proposals)

        return {
            "status": "WAITING_FOR_APPROVAL",
            "thread_id": thread_id,
            "proposals": [
                {
                    "proposal_id": p.proposal_id,
                    "action_type": p.action_type,
                    "status": p.status.name,
                    "payload": p.payload or {},
                }
                for p in saved_proposals
            ],
        }

    # -------------------------------
    # 🔥 RETURN ONLY LAST AI MESSAGE
    # -------------------------------
    final_messages = result.get("messages", [])

    last_ai_message = None

    for msg in reversed(final_messages):
        if isinstance(msg, AIMessage) and msg.content:
            last_ai_message = msg
            break

    if last_ai_message:
        return {
            "status": "COMPLETED",
            "thread_id": thread_id,
            "messages": [
                {"content": last_ai_message.content}
            ],
        }

    # fallback
    return {
        "status": "COMPLETED",
        "thread_id": thread_id,
        "messages": [
            {"content": "I couldn't generate a response."}
        ],
    }