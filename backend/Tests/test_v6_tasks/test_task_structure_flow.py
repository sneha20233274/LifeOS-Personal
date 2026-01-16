from langchain_core.messages import HumanMessage
from my_agent.chatstate import ChatState
from langgraph.types import Command
from my_agent.model_gen import chatbot 
from app.services.Executor.dispatcher import execute_proposals
from app.services.proposal_dependency_service import apply_dependencies
from app.services.proposal_service import save_proposals
from my_agent.models.action_proposal import ProposalStatus
import pprint
def test_task_structure_generation_end_to_end(db):
    """
    Integration test:
    - User gives a task creation prompt
    - LangGraph runs end-to-end
    - Tasks and subtasks are produced
    """
    thread_id = "threadg"

    # ---------------- STEP 1: START AGENT (INTERRUPT) ----------------
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    final_state = chatbot.invoke(
        {
            "messages": [HumanMessage(content="Create a task to complete agentic AI project in 10 days")],
            "iteration": 0,
            "max_iterations": 1,
        },
        config=config
    )
    

    assert "__interrupt__" in final_state
    pprint.pprint(final_state)

    proposals_data = final_state.get("proposals", [])
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

    # Basic sanity assertions
    
    assert len(final_state["routine_tasks"]) > 0

    # Validate structure shape
    print("Generated Tasks and Subtasks:", final_state["routine_tasks"])
