
from my_agent.chatstate import ChatState
from my_agent.llm import structured_fitness_planer_llm
from my_agent.schemas.fitness import FitnessPlan
from langchain_core.messages import SystemMessage, HumanMessage
import json
def fitness_planer_node(state: ChatState) -> ChatState:

    user_text = state["messages"][-1].content
    fitness_prompt = f"""

You are a Fitness Planner Agent.
Your task is to generate a complete, safe, and realistic fitness plan based on the user's goal.
User goal:
{user_text}
INSTRUCTIONS:
- Output ONLY valid JSON.
- Strictly follow the FitnessPlan schema below.
- Fill EVERY field — never omit any.
- Use sensible defaults when user doesn't specify.
- Assume user is healthy unless stated otherwise.
FITNESS PLAN SCHEMA (MUST MATCH EXACTLY):
{{ ... }}
DEFAULTS TO USE IF NOT SPECIFIED:
...
SAFETY RULES (ENFORCE):
OUTPUT ONLY THE JSON. NO explanations, no markdown, no extra text.

"""

    messages = [

        SystemMessage(

            content="You are a fitness plan generation engine. Output only valid JSON matching the schema."

        ),

        HumanMessage(content=fitness_prompt),

    ]

    print("Sending to fitness planner LLM...")


    result = structured_fitness_planer_llm.invoke(messages)
    print("Fitness Plan Generated:")
    return {

        **state,

        "fitness_plan": result.model_dump(),

        "approved": False,

    }

