from typing import  Annotated,List,Literal
from pydantic import BaseModel, Field
# ---------- Reusable constrained types ----------
Calories = Annotated[int, Field(ge=800, le=5000)]
Grams = Annotated[int, Field(ge=0, le=500)]
MealsPerDay = Annotated[int, Field(ge=1, le=8)]
WaterLiters = Annotated[float, Field(ge=0.5, le=10.0)]


# ---------- Sub-models ----------
class MacroSplit(BaseModel):
    protein_g: Grams
    carbs_g: Grams
    fats_g: Grams


class Hydration(BaseModel):
    water_liters: WaterLiters


class CheatMeals(BaseModel):
    allowed: bool
    frequency_per_week: Annotated[int, Field(ge=0, le=7)]


class DietConstraints(BaseModel):
    budget_level: Literal["low", "medium", "high"]
    cooking_time: Literal["low", "medium", "high"]


# ---------- Main Diet Plan ----------
class DietPlan(BaseModel):
    # --------------------------------------------------
    # Goal & calories
    # --------------------------------------------------
    goal: Literal["fat_loss", "maintenance", "muscle_gain"]
    daily_calories: Calories

    # --------------------------------------------------
    # Macros & meals
    # --------------------------------------------------
    macro_split: MacroSplit
    meal_frequency: MealsPerDay

    # --------------------------------------------------
    # Food preferences & restrictions
    # --------------------------------------------------
    diet_type: Literal["vegetarian", "non_veg", "vegan"]
    food_preferences: List[str] = Field(default_factory=list)
    food_avoidances: List[str] = Field(default_factory=list)

    # --------------------------------------------------
    # Sustainability & adherence
    # --------------------------------------------------
    flexibility: Literal["strict", "moderate", "flexible"]

    hydration: Hydration
    supplements: List[str] = Field(default_factory=list)

    # --------------------------------------------------
    # Lifestyle constraints
    # --------------------------------------------------
    cheat_meals: CheatMeals
    constraints: DietConstraints

    # --------------------------------------------------
    # Medical & safety
    # --------------------------------------------------
    medical_notes: List[str] = Field(default_factory=list)
