from my_agent.schemas.intentresolutionoutput import IntentResolutionOutput
from my_agent.schemas.goalcreate import GoalCreate
from my_agent.schemas.evalaution_schema import EvaluatorOutput
from my_agent.schemas.routine import RoutineLLMOutput
from my_agent.schemas.diet import DietPlan
from my_agent.schemas.fitness import FitnessPlan
from my_agent.schemas.activity import ActivityCreateList
from my_agent.schemas.analytics import AggregationOutput
from langchain_groq import ChatGroq
from my_agent.schemas.fitness import WeeklyFitnessRoutine
from langchain_core.tools import tool
from dotenv import load_dotenv
from my_agent.schemas.fitness import WeeklyFocus
from my_agent.schemas.fitness import (
    StrengthDetails,
    CardioDetails,
    MobilityDetails,
)
from my_agent.schemas.routine_structure import RoutineStructurerNodeResponse, PlanningDeciderOutput
from my_agent.schemas.fitness import DayTimelineSkeleton
from my_agent.tools.date_tools import (
    get_today_date,
    add_days_to_date
)

import os

load_dotenv()

# --------------------------------------------------
# GLOBAL API KEY (IMPORTANT)
# --------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm(model="openai/gpt-oss-120b", temperature=0.7):
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=GROQ_API_KEY
    )

# --------------------------------------------------
# Tools
# --------------------------------------------------
tools_date = [
    get_today_date,
    add_days_to_date
]

@tool
def json(**kwargs):
    """Transport-only tool for structured outputs."""
    return kwargs

# --------------------------------------------------
# Base LLMs
# --------------------------------------------------
base_llm = get_llm("openai/gpt-oss-120b", 0.7)

plan_mode = get_llm("openai/gpt-oss-120b", 0.3)\
    .bind_tools(tools_date)\
    .with_structured_output(PlanningDeciderOutput)

aggregation_llm = get_llm("openai/gpt-oss-120b", 0.1)
analysis_llm = get_llm("openai/gpt-oss-120b", 0.5)

goal_prompt_llm = get_llm("llama-3.1-8b-instant", 0.1)

evaluator_llm = get_llm("openai/gpt-oss-120b", 0.3)
routine_llm = get_llm("openai/gpt-oss-120b", 0.3)
fitness_planner_llm = get_llm("openai/gpt-oss-120b", 0.3)

# --------------------------------------------------
# Structured Outputs
# --------------------------------------------------
goal_prompt_structured_llm = (
    goal_prompt_llm
    .bind_tools([json])
    .with_structured_output(GoalCreate)
)

intent_resolver_llm = (
    base_llm
    .bind_tools([json])
    .with_structured_output(IntentResolutionOutput)
)

evaluator_structured_llm = (
    evaluator_llm
    .bind_tools([json])
    .with_structured_output(EvaluatorOutput)
)

routine_structured_llm = (
    routine_llm
    .bind_tools([json])
    .with_structured_output(RoutineLLMOutput)
)

diet_planer_llm = (
    routine_llm
    .bind_tools([json])
    .with_structured_output(DietPlan)
)

structured_fitness_planer_llm = (
    fitness_planner_llm
    .bind_tools([json])
    .with_structured_output(FitnessPlan)
)

weekly_focus_llm = (
    get_llm("openai/gpt-oss-120b", 0.1)
    .bind_tools([json])
    .with_structured_output(WeeklyFocus)
)

day_timeline_llm = (
    get_llm("openai/gpt-oss-120b", 0.2)
    .bind_tools([json])
    .with_structured_output(DayTimelineSkeleton)
)

strength_detail_llm = (
    get_llm("openai/gpt-oss-120b", 0.2)
    .bind_tools([json])
    .with_structured_output(StrengthDetails)
)

cardio_detail_llm = (
    get_llm("openai/gpt-oss-120b", 0.2)
    .bind_tools([json])
    .with_structured_output(CardioDetails)
)

mobility_detail_llm = (
    get_llm("openai/gpt-oss-120b", 0.2)
    .bind_tools([json])
    .with_structured_output(MobilityDetails)
)

activity_structured_llm = (
    base_llm
    .bind_tools([json])
    .with_structured_output(ActivityCreateList)
)

analytics_structured_llm = (
    aggregation_llm
    .with_structured_output(AggregationOutput)
)

routine_structurer_llm = (
    analysis_llm
    .bind_tools([json])
    .with_structured_output(RoutineStructurerNodeResponse)
)