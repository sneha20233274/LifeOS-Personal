
from langchain_core.messages import HumanMessage
from langchain_core.messages import HumanMessage
from my_agent.chatstate import ChatState
from langgraph.types import Command
from my_agent.model_gen import chatbot 
from my_agent.chatstate import ChatState



def test_weekly_fitness_routine_generation():
    """
    End-to-end test:
    User prompt -> fitness plan -> weekly time-wise routine
    """

    initial_state: ChatState = {
        "messages": [
            HumanMessage(
                content=(
                    "I want a muscle gain fitness routine. "
                    "I work out from 9am to 10am. "
                    "Monday leg day, Tuesday push day, Wednesday rest. "
                    "Include warmup, exercises, breaks, cooldown."
                )
            )
        ],
        "intent": "fitness",
        "iteration": 0,
        "max_iterations": 2,
        "approved": False,
        "requires_execution": False,  # prevent DB execution in test
    }

    final_state = chatbot.invoke(
        initial_state,
        config={
            "configurable": {
                "user_id": 123
            }
        }
    )

    # ---------------- ASSERTIONS ----------------

    assert "weekly_routine" in final_state, "weekly_routine not found in state"

    weekly_routine = final_state["weekly_routine"]

    # Basic shape
    assert "schedule" in weekly_routine
    assert isinstance(weekly_routine["schedule"], dict)

    # Must have at least Monday
    assert "monday" in weekly_routine["schedule"]

    monday = weekly_routine["schedule"]["monday"]

    assert "timeline" in monday
    assert isinstance(monday["timeline"], dict)

    # Time-wise keys like "09:00-09:15"
    time_keys = list(monday["timeline"].keys())
    assert len(time_keys) > 0

    for key in time_keys:
        assert "-" in key, f"Invalid time slot key: {key}"
        start, end = key.split("-")
        assert len(start) == 5 and len(end) == 5  # HH:MM

    # Ensure at least one exercise block exists
    blocks = monday["timeline"].values()
    has_exercise = any(
        block["block_type"] == "exercise" for block in blocks
    )
    assert has_exercise, "No exercise block found in Monday routine"
