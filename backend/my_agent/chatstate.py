from typing import Optional, TypedDict, Annotated, Dict, Any, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from app.utils.dictionary_merger import update_dict
from my_agent.schemas.activity import ActivityCreate


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
   
    # UPDATED: Wrapped in Annotated with update_dict so they merge automatically
    metric_result: Annotated[Dict[str, Any], update_dict]
    comparison_result: Annotated[Dict[str, Any], update_dict]
   
    # loop / control info
    iteration: int
    max_iterations: int
