from typing import Optional, TypedDict, Annotated, Dict, Any, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from app.utils.dictionary_merger import update_dict
from my_agent.schemas.activity import ActivityCreate
from my_agent.schemas.routine_structure import PlanningDeciderOutput, DailyContext

class ChatState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]

    intent: str

    structured_goal: Dict[str, Any]   # GoalCreate output
    routine_tasks: List[Dict[str, Any]]

    fitness_plan: Dict[str, Any]        # active fitness plan only
    diet_plan: Dict[str, Any]           # active diet plan only

        # NEW
    requires_execution: bool
    proposals: List[Dict[str, Any]]   # pure data, no DB logic
    execution_result: Optional[Dict[str, Any]]
    
    activity_create: List[ActivityCreate]
    feedback: str
    approved: bool

    # --- Aggregation phase ---
    aggregation_spec: Optional[Dict[str, Any]]
    aggregation_result: Optional[Dict[str, Any] | float]
    weekly_focus: Dict[str, str]             # monday → focus
    day_timelines: Dict[str, Dict[str, Any]] # monday → timeline skeleton
    weekly_routine: Optional[Dict[str, Any]] 
   
    # UPDATED: Wrapped in Annotated with update_dict so they merge automatically
    metric_result: Annotated[Dict[str, Any], update_dict]
    comparison_result: Annotated[Dict[str, Any], update_dict]
   
    planning_decision: Optional[PlanningDeciderOutput] = None
    daily_context: Optional[DailyContext] = None
    routine_structure: Optional[dict] = None
    # loop / control info
    iteration: int
    max_iterations: int
