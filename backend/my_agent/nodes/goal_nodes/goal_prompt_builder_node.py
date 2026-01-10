
from my_agent.llm import goal_prompt_structured_llm
from my_agent.chatstate import ChatState
from my_agent.schemas.goalcreate import GoalCreate
from my_agent.prompts.goal_system_prompt import GOAL_PROMPT_SYSTEM
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def goal_prompt_builder_node(state:ChatState
) -> ChatState:
    """
    Converts user input into GoalCreate schema.
    """
    print("Routine generator node input state")
    user_text = state["messages"][-1].content

    messages = [
        SystemMessage(content=GOAL_PROMPT_SYSTEM),
        HumanMessage(content=user_text),
    ]
    print("Messages to goal LLM:", messages)
    goal: GoalCreate = goal_prompt_structured_llm.invoke(messages)
    print("Goal LLM output:", goal)
    # update state with structured goal
    new_state = {
        **state,
        "structured_goal": goal.model_dump()
    }

    # optional: confirmation message for UI
    confirmation = (
        "I’ve understood your goal as:\n\n"
        f"🎯 Goal: {goal.goal_name}\n"
        f"📝 Description: {goal.description or '—'}\n"
        f"📅 Target Date: {goal.target_date or 'Not specified'}\n"
        f"⭐ Importance Level: {goal.importance_level}/5\n"
    )

    if goal.motivations:
        confirmation += "💡 Motivations:\n"
        for m in goal.motivations:
            confirmation += f"• {m}\n"

    new_state["messages"] = [
        AIMessage(content=confirmation)
    ]

    return new_state