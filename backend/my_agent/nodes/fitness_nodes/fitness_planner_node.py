# from my_agent.chatstate import ChatState
# from my_agent.llm import structured_fitness_planer_llm
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# def fitness_planer_node(state: ChatState) -> ChatState:
#     user_text = state["messages"][-1].content

#     fitness_prompt = f"""
# You are a Fitness Planner Agent.

# Your task is to generate a complete, safe, and realistic fitness plan based on the user's goal.

# User goal:
# {user_text}

# INSTRUCTIONS:
# - Output ONLY valid JSON.
# - Strictly follow the FitnessPlan schema below.
# - Fill EVERY field — never omit any.
# - Use sensible defaults when user doesn't specify.
# - Assume user is healthy unless stated otherwise.

# FITNESS PLAN SCHEMA (MUST MATCH EXACTLY):
# {{
#   "goal": "fat_loss" or "muscle_gain" or "endurance",
#   "experience_level": "beginner" or "intermediate" or "advanced",

#   "weekly_frequency": integer between 1 and 7,
#   "session_duration_min": integer between 15 and 180,

#   "training_split": "full_body" or "upper_lower" or "push_pull_legs",
#   "workout_types": array of "strength", "cardio", "mobility" (at least one),

#   "intensity": {{
#     "level": "low" or "moderate" or "high",
#     "rpe_range": [min_rpe, max_rpe] where each is integer 1-10
#   }},

#   "weekly_structure": {{
#     "workout_days": integer 1-7 (must equal weekly_frequency),
#     "rest_days": integer 0-6 (must make total 7 days with workout_days)
#   }},

#   "exercise_preferences": array of strings (e.g. ["dumbbells", "bodyweight"]),
#   "exercise_constraints": array of strings (e.g. ["knee pain", "no gym"]),

#   "progression_strategy": "linear" or "wave" or "autoregulatory",

#   "recovery": {{
#     "sleep_hours": integer 4-12,
#     "active_recovery": true or false
#   }},

#   "safety_notes": array of strings,
#   "compliance_level": "strict" or "flexible"
# }}

# DEFAULTS TO USE IF NOT SPECIFIED:
# - experience_level: "beginner"
# - weekly_frequency: 3
# - session_duration_min: 45
# - training_split: "full_body"
# - workout_types: ["strength", "mobility"]
# - intensity: {{"level": "moderate", "rpe_range": [6, 8]}}
# - progression_strategy: "linear"
# - recovery: {{"sleep_hours": 8, "active_recovery": true}}
# - compliance_level: "flexible"
# - All arrays: []

# SAFETY RULES (ENFORCE):
# - Beginners: max 4 workout days, no "high" intensity
# - RPE max ≤8 for beginners/intermediate, ≤10 for advanced
# - workout_days + rest_days must = 7
# - workout_days must equal weekly_frequency

# OUTPUT ONLY THE JSON. NO explanations, no markdown, no extra text.
# """

#     messages = [
#         SystemMessage(content="You are a fitness plan generation engine. Output only valid JSON matching the schema."),
#         HumanMessage(content=fitness_prompt)
#     ]

#     print("Sending to fitness planner LLM...")
#     llm_output = structured_fitness_planer_llm.invoke(
#     messages,
#     config={
#         "tool_choice": "FitnessPlan"  # MUST match your schema/tool name
#     }
# )

#     print("Fitness Plan Generated:")

#     print(llm_output.model_dump_json(indent=2))
#     # Store as dict (safe and serializable)
#     return {
#         **state,
#         "fitness_plan": llm_output.model_dump(),  # ← dict, not model object
#         "messages": state["messages"] 
#     }
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
          ...

          OUTPUT ONLY THE JSON. NO explanations, no markdown, no extra text.
          """

    messages = [
        SystemMessage(
            content= "You MUST call the tool FitnessPlan.\n"
                      "Do NOT return JSON text.\n"
                      "Do NOT explain.\n"
                      "Only call the tool with valid arguments."
        ),
        HumanMessage(content=fitness_prompt),
    ]

    print("Sending to fitness planner LLM...")

    # ✅ DO NOT FORCE TOOL
    result = structured_fitness_planer_llm.invoke(messages)



   

    return {
        **state,
        "fitness_plan": result.model_dump(),
        "approved": False,
    }
