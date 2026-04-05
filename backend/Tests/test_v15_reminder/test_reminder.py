import pprint
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from my_agent.model_gen import chatbot
from my_agent.models.action_proposal import ProposalStatus

from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from app.services.Executor.dispatcher import execute_proposals


def test_interrupt_approve_resume_routine_schedule(db):
    """
    End-to-end test for:
    - Daily routine planning
    - Proposal interrupt
    - Human approval
    - Execution
    - Graph resume
    """

    # ---------------------------
    # STEP 0: Test config
    # ---------------------------
    thread_id = "routine-scheduling-d"
    user_id = 5

    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id,
            "db": db,
        }
    }

    # ---------------------------
    # STEP 1: Invoke agent (expect interrupt)
    # ---------------------------
    result = chatbot.invoke(
        {
            "messages": [
                HumanMessage(
                    content="i have a meating in evening from 4 to 6 on 21 and from 11 to 1 i have to meet someone so generate schedule for that"
                )
            ],
            "iteration": 0,
            "max_iterations": 1,
        },
        config=config,
    )

    # ---- interrupt must happen
    assert "__interrupt__" in result
    pprint.pprint(result)

    proposals_data = result.get("proposals", [])
    assert proposals_data, "Expected scheduling proposals on interrupt"

    # ---- ensure at least one scheduling proposal exists
    assert any(
        p["action_type"] == "schedule_routine_event"
        for p in proposals_data
    ), "Expected schedule_routine_event proposal"

    # ---------------------------
    # STEP 2: Save proposals
    # ---------------------------
    saved = save_proposals(
        db=db,
        thread_id=thread_id,
        user_id=user_id,
        proposals=proposals_data,
    )

    # ---- apply dependency resolution (temp keys)
    apply_dependencies(db, saved)

    # ---------------------------
    # STEP 3: Human approves all proposals
    # ---------------------------
    for proposal in saved:
        proposal.status = ProposalStatus.APPROVED

    db.commit()

    # ---------------------------
    # STEP 4: Execute approved proposals
    # ---------------------------
    execution_result = execute_proposals(
        db=db,
        proposals=saved,
    )

    assert execution_result["executed"], "Expected execution to occur"

    # ---- ensure routine events were executed
    executed_actions = execution_result.get("executed_actions", [])
    assert any(
        action["action_type"] == "schedule_routine_event"
        for action in executed_actions
    ), "Expected routine scheduling execution"

    # ---------------------------
    # STEP 5: Resume graph
    # ---------------------------
    resumed = chatbot.invoke(
        Command(resume=True),
        config=config,
    )

    # ---------------------------
    # STEP 6: Assert graph completed
    # ---------------------------
    assert "__interrupt__" not in resumed
    assert "messages" in resumed

    final_messages = resumed["messages"]
    assert len(final_messages) >= 1

    # Optional semantic check (soft)
    # last_message = final_messages[-1].content.lower()
    # assert "routine" in last_message or "scheduled" in last_message
