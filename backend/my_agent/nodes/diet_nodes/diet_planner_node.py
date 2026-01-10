from my_agent.chatstate import ChatState
from my_agent.llm import diet_planer_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def diet_planer_node(state: ChatState) -> ChatState:
    """
    Generates a personalized diet plan based on the user's goal using structured output.
    """
    user_text = state["messages"][-1].content

    diet_prompt = f"""
You are a professional Diet Planner Agent.

Create a safe, sustainable diet plan based on the user's goal.

User input:
{user_text}

INSTRUCTIONS:
- Output ONLY valid JSON.
- Include every field in the schema below.
- No explanations, no markdown, no extra text.

SCHEMA (must match exactly):
{{
  "goal": "fat_loss" or "maintenance" or "muscle_gain",
  "daily_calories": integer 800-5000,

  "macro_split": {{
    "protein_g": integer 0-500,
    "carbs_g": integer 0-500,
    "fats_g": integer 0-500
  }},

  "meal_frequency": integer 1-8,
  "diet_type": "vegetarian" or "non_veg" or "vegan",
  "food_preferences": [],
  "food_avoidances": [],
  "flexibility": "strict" or "moderate" or "flexible",
  "hydration": {{"water_liters": float 0.5-10.0}},
  "supplements": [],
  "cheat_meals": {{"allowed": true or false, "frequency_per_week": integer 0-7}},
  "constraints": {{"budget_level": "low" or "medium" or "high", "cooking_time": "low" or "medium" or "high"}},
  "medical_notes": []
}}

DEFAULTS (if not specified):
- goal: "maintenance"
- daily_calories: 2200
- macro_split: protein_g=120, carbs_g=250, fats_g=70
- meal_frequency: 3
- diet_type: "vegetarian"
- flexibility: "moderate"
- hydration.water_liters: 3.0
- cheat_meals: {{"allowed": true, "frequency_per_week": 1}}
- supplements: []
- All arrays: []

SAFETY RULES:
- Protein and fats > 0 unless medically justified
- If cheat_meals.allowed = false → frequency_per_week = 0
- Calories should match goal roughly

OUTPUT ONLY THE JSON. NOTHING ELSE.
"""

    messages = [
        SystemMessage(content="You are a diet plan engine. Return only valid JSON."),
        HumanMessage(content=diet_prompt)
    ]

    print("Sending request to Diet Planner LLM...")

    llm_output = diet_planer_llm.invoke(messages)

    # CRITICAL: SAFE PRINTING ONLY
    print("Diet Plan Generated Successfully:")
    print(llm_output.model_dump_json(indent=2))   # This is 100% safe

    # Optional: just print the object (also safe)
    # print(llm_output)

    # Update state
    new_state = {
        **state,
        "diet_plan": llm_output.model_dump(),  # store as dict
        "messages": state["messages"] + [
            AIMessage(content="I've created a personalized diet plan for you! Let me know if you'd like adjustments.")
        ]
    }

    return new_state