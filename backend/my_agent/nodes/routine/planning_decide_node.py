from my_agent.llm import plan_mode
from langchain_core.messages import SystemMessage,HumanMessage
from my_agent.chatstate import ChatState

def build_planning_decider_human_message(user_prompt: str) -> HumanMessage:
    """
    Human message for planning_decider_node.

    Purpose:
    - Let AI interpret the user's intent strength and date reference
    - No planning, no execution, no extra context
    """
    return HumanMessage(
        content=f"""
User request:
{user_prompt}

Decide:
- planning_mode
- fixed_events_present
- target_date (as a concrete YYYY-MM-DD date)
"""
    )

PLANNING_DECIDER_SYSTEM_MESSAGE = SystemMessage(
    content="""
You are a planning_decider_node.

Your task is to interpret the user's request and decide HOW the system should behave.

You MUST decide:
1. planning_mode
2. fixed_events_present
3. target_date

CRITICAL RULES:
- target_date MUST be a concrete calendar date in YYYY-MM-DD format.
- You MUST resolve relative phrases such as:
  "today", "tomorrow", "after 3 days", "next Monday", etc.
  into an exact date.
- You MUST NOT output relative phrases or descriptions.
- If the user refers to a day ambiguously, choose the most reasonable upcoming date.

You do NOT plan tasks.
You do NOT optimize schedules.
You ONLY classify behavior and resolve the date.

Output must strictly match the provided schema.
No explanations. No extra fields.
"""
)
def planning_decider_node(state: ChatState) -> ChatState:
    """
    AI-powered node that decides planning behavior and resolves target date.
    Uses structured output to guarantee correctness.
    """

    
    user_prompt = state["messages"][-1].content
    response = plan_mode.invoke(
        [
            PLANNING_DECIDER_SYSTEM_MESSAGE,
            build_planning_decider_human_message(
                user_prompt= user_prompt
            )
        ]
    )

    return {
        "planning_decision": response
    }