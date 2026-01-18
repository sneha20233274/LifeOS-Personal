from langchain_core.messages import HumanMessage
from langgraph.types import Command
import pprint

from my_agent.model_gen import chatbot
from my_agent.models.action_proposal import ProposalStatus
from app.services.Executor.dispatcher import execute_proposals
from app.services.proposal_dependency_service import apply_dependencies
from app.services.proposal_service import save_proposals

from app.models.criteria import Criteria


def test_task_structure_generation_end_to_end(db):
    """
    Integration test:
    - Seed criteria
    - User logs an activity
    - LangGraph runs end-to-end
    - Activity is created   using real criteria IDs
    """

    # -------------------------------------------------
    # STEP 0: SEED CRITERIA (IMPORTANT)
    # -------------------------------------------------
    criteria_seed = [
        Criteria(name="coding", description="Writing or modifying code"),
        Criteria(name="debugging", description="Fixing bugs or errors"),
        Criteria(name="reading", description="Reading documentation or articles"),
        Criteria(name="youtube", description="Watching technical videos"),
    ]

    db.add_all(criteria_seed)
    db.commit()

    # Optional: sanity check
    assert db.query(Criteria).count() == 4

    # -------------------------------------------------
    # STEP 1: START AGENT (INTERRUPT EXPECTED)
    # -------------------------------------------------
    thread_id = "threadi"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    final_state = chatbot.invoke(
        {
            "messages": [
                HumanMessage(
                    content="log an activity for coding from 3 pm to 5 pm"
                )
            ],
            "iteration": 0,
            "max_iterations": 1,
            
        },
        config=config
    )

    assert "__interrupt__" in final_state
    pprint.pprint(final_state)

    proposals_data = final_state.get("proposals", [])
    assert proposals_data, "Expected proposals on interrupt"

    # -------------------------------------------------
    # STEP 2: SAVE PROPOSALS
    # -------------------------------------------------
    saved = save_proposals(
        db=db,
        thread_id=thread_id,
        user_id=1,
        proposals=proposals_data
    )

    apply_dependencies(db, saved)

    # -------------------------------------------------
    # STEP 3: HUMAN APPROVES ALL
    # -------------------------------------------------
    for p in saved:
        p.status = ProposalStatus.APPROVED
    db.commit()

    # -------------------------------------------------
    # STEP 4: EXECUTE APPROVED PROPOSALS
    # -------------------------------------------------
    execution_result = execute_proposals(
        db=db,
        proposals=saved
    )

    assert execution_result["executed"], "Expected execution to happen"

    # -------------------------------------------------
    # STEP 5: RESUME GRAPH
    # -------------------------------------------------
    resumed = chatbot.invoke(
        Command(resume=True),
        config=config,
    )

    # -------------------------------------------------
    # STEP 6: ASSERT GRAPH COMPLETED
    # -------------------------------------------------
    assert "__interrupt__" not in resumed
    assert "messages" in resumed

    final_messages = resumed["messages"]
    assert len(final_messages) >= 1

    # -------------------------------------------------
    # STEP 7: ASSERT ACTIVITY CREATED
    # -------------------------------------------------
    from app.models.activity import Activity

    activities = db.query(Activity).all()
    assert activities, "Expected at least one activity in DB"

    activity = activities[0]

    assert activity.duration_minutes > 0
    assert activity.summary_category is not None

    # criteria relationship should work
    assert activity.criteria is not None
    # could be empty or non-empty depending on LLM confidence
