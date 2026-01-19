from my_agent.chatstate import ChatState
from my_agent.llm import (
    strength_detail_llm,
    cardio_detail_llm,
    mobility_detail_llm,
)


def fitness_optimisor_node(state: ChatState) -> ChatState:
    """
    Optimises ONLY timeslot details based on evaluator feedback.
    """
    weekly_routine = state["weekly_routine"]
    feedback = state["feedback"]

    schedule = weekly_routine["schedule"]

    for day, day_data in schedule.items():
        for _, block in day_data["timeline"].items():
            category = block["category"]

            # Break / rest blocks are untouched
            if category == "none":
                continue

            if category == "strength":
                improved = strength_detail_llm.invoke(
                    f"""
Improve this strength exercise based on feedback.

Current details:
{block["details"]}

Evaluator feedback:
{feedback}

Rules:
- Modify only sets, reps, or exercise choice
- Keep muscle_group consistent
"""
                )
                block["details"] = improved.model_dump()

            elif category == "cardio":
                improved = cardio_detail_llm.invoke(
                    f"""
Improve this cardio activity based on feedback.

Current details:
{block["details"]}

Evaluator feedback:
{feedback}
"""
                )
                block["details"] = improved.model_dump()

            elif category == "mobility":
                improved = mobility_detail_llm.invoke(
                    f"""
Improve this mobility drill based on feedback.

Current details:
{block["details"]}

Evaluator feedback:
{feedback}
"""
                )
                block["details"] = improved.model_dump()

    iteration = state.get("iteration", 0) + 1

    return {
        **state,
        "weekly_routine": weekly_routine,  # already valid
        "iteration": iteration,
        "approved": False,
    }
