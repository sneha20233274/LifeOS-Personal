from typing import Optional, TypedDict, Annotated, Dict, Any, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
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

   
    # loop / control info
    iteration: int
    max_iterations: int
