from uuid import uuid4
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage

from my_agent.model_gen import chatbot
# Your LangGraph / LangChain agent graph.
from app.services.proposal_service import save_proposals
# Function to save proposals into DB.

# Starts a LangGraph / LangChain agent run, tracks it with a thread ID, 
# handles interruptions, and stores AI-generated action proposals for human approval.
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
        # LangGraph uses this to store memory per thread.
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
        # This inserts proposals into ActionProposal table.
        # Agent decided it must pause for human approval.

        return {
            "thread_id": thread_id,
            "status": "WAITING_FOR_APPROVAL",
            "proposals_created": len(proposals)
        }
    #   Frontend now knows:
    # • Show approval UI
    # • Pause agent

    return {
        "thread_id": thread_id,
        "status": "COMPLETED"
    }
