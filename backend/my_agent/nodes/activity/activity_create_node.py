from my_agent.chatstate import ChatState
from my_agent.llm import activity_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage

CRITERIA_CATALOG = """
1: coding – writing or modifying code
2: debugging – fixing bugs or errors
3: reading – reading documentation or articles
4: youtube – watching videos
5: meeting – calls or discussions
6: exercise_cardio – cardio exercise
7: exercise_strength – strength training
"""


def activity_create_node(state: ChatState) -> ChatState:
    """
    Create activity records from a human activity log.
    Uses a manually seeded criteria catalog (no DB access).
    """

    user_text = state["messages"][-1].content

    activity_prompt = f"""
You are an activity logging engine.

User input:
"{user_text}"

Convert the input into one or more activity records
representing actions that have ALREADY happened.

SUMMARY CATEGORY (MANDATORY):
Choose EXACTLY ONE from (case-sensitive):
work
learning
exercise
admin
leisure
sleep
social
commute
other

CRITERIA (OPTIONAL):
You may assign criteria ONLY from the list below.
Use the corresponding criteria_id values.
If none apply confidently, return an empty list [].

AVAILABLE CRITERIA:
{CRITERIA_CATALOG}

TIME RULES:
- duration_minutes must be a positive integer (> 0)
- If start/end times are not explicit, set them to null
- Do NOT assign deadlines or future times

FORBIDDEN:
- Do NOT create tasks, subtasks, goals, or plans
- Do NOT invent new criteria
"""

    messages = [
        SystemMessage(
            content="You convert human activity descriptions into structured activity records."
        ),
        HumanMessage(content=activity_prompt),
    ]

    # Structured output bound to ActivityCreateList
    result = activity_structured_llm.invoke(messages)

    return {
        **state,
        "activity_create": result.activities
    }
