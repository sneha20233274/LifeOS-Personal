from typing import TypedDict, Annotated, Dict, Any, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
class ChatState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]

    intent: str

    structured_goal: Dict[str, Any]   # GoalCreate output
    routine_tasks: List[Dict[str, Any]]

    fitness_plan: Dict[str, Any]        # active fitness plan only
    diet_plan: Dict[str, Any]           # active diet plan only

    feedback: str
    approved: bool

    # loop / control info
    iteration: int
    max_iterations: int
