from langchain_core.messages import SystemMessage, HumanMessage


DAILY_ROUTINE_PLANNER_SYSTEM_MESSAGE = SystemMessage(
    content="""
You are a daily routine planner.

Your task is to generate the FINAL routine for the day.
Your output will be shown directly to the user and WILL NOT be re-planned.

You are given:
- Existing scheduled events (locked, cannot move)
- Candidate work items (subtasks with priority signals)
- The user's request
- The target date

RULES (DO NOT BREAK):
1. You MUST respect all existing scheduled events.
2. You MUST NOT create overlapping events.
3. You MUST decide start_time and end_time for every event.
4. You MUST output events in valid JSON matching the schema exactly.
5. You MUST generate a unique temp_event_key for each event.
6. You MUST NOT include any fields outside the schema.
7. You MUST NOT ask questions or include explanations.
8. You MUST assume the user may edit the result later, but YOU WILL NOT be re-run.

PLANNING BEHAVIOR:
- If the user explicitly asked to schedule something, it has highest priority.
- Otherwise, select subtasks based on priority_score.
- Prefer higher goal importance, then task difficulty.
- Do not overload the day; produce a realistic routine.

TIME GUIDELINES:
- Use reasonable working hours.
- Group similar work where appropriate.
- Leave gaps between long sessions when possible.

SOURCE:
- Always set source = "ai".

OUTPUT:
You MUST return a JSON object of this exact form:

{
  "events": [ ... ]
}

No text. No markdown. No commentary.
"""
)

import json

def build_daily_routine_planner_human_message(daily_context, user_prompt):
    # ✅ Handle both dict and pydantic
    if hasattr(daily_context, "model_dump"):
        daily_context = daily_context.model_dump()

    return HumanMessage(
        content=f"""
User request:
{user_prompt}

Daily context (facts, not decisions):
{json.dumps(daily_context, default=str)}
"""
    )

from my_agent.llm import routine_structurer_llm
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import PydanticOutputParser

from my_agent.llm import routine_structurer_llm 
from my_agent.chatstate import ChatState


def daily_routine_planner_node(state: dict) -> dict:
    """
    Merged planner + structurer node.
    """

    # ✅ SAFE ACCESS
    daily_context = state.get("daily_context")
    if not daily_context:
        raise ValueError("daily_context missing in state")

    # ✅ CORRECT WAY TO GET USER PROMPT
    user_prompt = state["messages"][-1].content

    # ✅ LLM CALL
    response = routine_structurer_llm.invoke(
        [
            DAILY_ROUTINE_PLANNER_SYSTEM_MESSAGE,
            build_daily_routine_planner_human_message(
                daily_context=daily_context,
                user_prompt=user_prompt
            )
        ]
    )

    return {
        "routine_structure": response
    }
