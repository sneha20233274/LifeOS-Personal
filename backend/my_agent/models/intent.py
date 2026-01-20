from enum import Enum


class Intent(str, Enum):
    GOAL = "goal"
    TASK = "task"
   
    FITNESS = "fitness"
    DIET = "diet"
    LOGGING = 'activity_create'
    PLAN_DAY = "plan_day"
    SCHEDULING = "scheduling"
    ANALYZE = "analytics"
    ASK_REFLECTION = "ask_reflection"

    UPDATE_FITNESS_PLAN = "update_fitness_plan"
    UPDATE_DIET_PLAN = "update_diet_plan"

    GENERAL_QUERY = "general_query"
