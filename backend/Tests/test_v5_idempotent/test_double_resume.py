from langchain_core.messages import HumanMessage

from my_agent.model_gen import chatbot
from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from app.services.Executor.dispatcher import execute_proposals

from my_agent.models.action_proposal import ActionProposal, ProposalStatus
from app.models.task import Task
from langgraph.types import Command
def test_double_resume_is_idempotent(db):
    thread_id = "double-resume-thread-1"

    # ---------------- STEP 1: START AGENT (INTERRUPT) ----------------
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    result = chatbot.invoke(
        {
            "messages": [HumanMessage(content="Create a simple goal with one task")],
            "iteration": 0,
            "max_iterations": 1,
        },
        config=config
    )

    assert "__interrupt__" in result
    proposals_data = result["proposals"]
    assert proposals_data

    # ---------------- STEP 2: SAVE PROPOSALS ----------------

    saved = save_proposals(
        db=db,
        thread_id=thread_id,
        user_id=1,
        proposals=proposals_data
    )

    apply_dependencies(db, saved)

    # ---------------- STEP 3: APPROVE ALL ----------------

    for p in saved:
        p.status = ProposalStatus.APPROVED
    for p in saved:
        print(f"Proposal ID: {p.proposal_id}, Status: {p.status}")
    db.commit()

    # ---------------- STEP 4: FIRST RESUME ----------------

    execution_result_1 = execute_proposals(db=db, proposals=saved)

    assert execution_result_1["executed"], "Expected execution on first resume"

    # Resume graph
   
    chatbot.invoke(
        Command(resume=True),
        config=config
    )
    # Capture DB state
    task_count_after_first = db.query(Task).count()
    assert task_count_after_first > 0

    # ---------------- STEP 5: SECOND RESUME (NO-OP) ----------------

    execution_result_2 = execute_proposals(db=db, proposals=saved)

    # NOTHING should execute again
    assert execution_result_2["executed"] == []
    

    # Resume graph again
    chatbot.invoke(
        Command(resume=True),
        config=config
    )

    # ---------------- STEP 6: ASSERT NO DUPLICATES ----------------

    task_count_after_second = db.query(Task).count()
    assert task_count_after_second == task_count_after_first

