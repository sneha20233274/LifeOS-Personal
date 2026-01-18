from my_agent.model_gen import chatbot
from langchain_core.messages import HumanMessage
from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from app.services.Executor.dispatcher import execute_proposals
from my_agent.models.action_proposal import ProposalStatus
import pprint
from langgraph.types import Command



def test_interrupt_approve_resume(db):
    # -------- STEP 1: START AGENT (INTERRUPT EXPECTED) --------
    thread_id = "test-thread-123"
    user_id = 1
    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id
        }
    }


    result = chatbot.invoke(
        {
            "messages": [HumanMessage(content="Create a simple goal ")],
            "iteration": 0,
            "max_iterations": 1,
        },
        config=config
    )

    # Assert interrupt happened
    assert "__interrupt__" in result
    pprint.pprint(result)
    proposals_data = result.get("proposals", [])
    assert proposals_data, "Expected proposals on interrupt"

    # -------- STEP 2: SAVE PROPOSALS --------

    saved = save_proposals(
        db=db,
        thread_id=thread_id,
        user_id=1,
        proposals=proposals_data
    )

    apply_dependencies(db, saved)

    # -------- STEP 3: HUMAN APPROVES ALL --------

    for p in saved:
        p.status = ProposalStatus.APPROVED
    db.commit()

    # -------- STEP 4: EXECUTE APPROVED PROPOSALS --------

    execution_result = execute_proposals(
        db=db,
        proposals=saved
    )
    
    assert execution_result["executed"], "Expected execution to happen"

    # -------- STEP 5: RESUME GRAPH --------

   
    resumed = chatbot.invoke(
        Command(resume=True),
        config=config
    )
    # -------- STEP 6: ASSERT GRAPH COMPLETED --------

    assert "__interrupt__" not in resumed
    assert "messages" in resumed

    final_messages = resumed["messages"]
    assert len(final_messages) >= 1

    # last_message = final_messages[-1].content.lower()
    # assert "executed" in last_message or "completed" in last_message
