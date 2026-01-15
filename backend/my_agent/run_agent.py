from uuid import uuid4
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage

from my_agent.model_gen import chatbot
from app.services.proposal_service import save_proposals


def run_agent(
    *,
    user_input: str,
    user_id: int,
    db: Session
):
    thread_id = str(uuid4())

    result = chatbot.invoke(
        {
            "messages": [HumanMessage(content=user_input)],
            "iteration": 0,
            "max_iterations": 3,
        },
        config={"thread_id": thread_id}
    )

    # 🔴 Interrupted → save proposals
    if result.get("__interrupt__"):
        proposals = result.get("proposals", [])

        save_proposals(
            db=db,
            thread_id=thread_id,
            user_id=user_id,
            proposals=proposals
        )

        return {
            "thread_id": thread_id,
            "status": "WAITING_FOR_APPROVAL",
            "proposals_created": len(proposals)
        }

    return {
        "thread_id": thread_id,
        "status": "COMPLETED"
    }
