from datetime import date,datetime
from typing import Optional
from pydantic import BaseModel, Field



from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


class RoutineEventStructureSchema(BaseModel):
    """
    AI-produced routine event structure.
    This is NOT persisted directly.
    """

    temp_event_key: str = Field(
        ...,
        description="Temporary identifier for linking before DB IDs exist."
    )

    title: str = Field(..., max_length=255)
    description: Optional[str] = None

    start_time: datetime
    end_time: datetime
    is_all_day: bool = False

    category: str = Field(default="General")
    priority: Literal["Low", "Medium", "High"] = "Medium"

    location_or_link: Optional[str] = None

    source: Literal["ai"] = "ai"

    

from typing import List
from pydantic import BaseModel


class RoutineStructurerNodeResponse(BaseModel):
    """
    Final output of routine_structurer_node.
    """
    events: List[RoutineEventStructureSchema]

class PlanningDeciderOutput(BaseModel):
    planning_mode: Literal[
        "schedule_only",
        "mixed",
        "full_planning"
    ]
    fixed_events_present: bool
    target_date: date
    confidence: float


from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


class ExistingEventContext(BaseModel):
    event_id: int
    title: str
    start_time: datetime
    end_time: datetime
    category: Optional[str]


class TaskContext(BaseModel):
    task_id: int
    task_name: str
    difficulty: int


class GoalContext(BaseModel):
    goal_id: int
    goal_name: str
    importance_level: int
    target_date: Optional[date]


class CandidateWorkItem(BaseModel):
    subtask_id: int
    subtask_name: str
    subtask_type: str
    weight: int

    task: TaskContext
    goal: Optional[GoalContext]

    priority_score: int


class DailyContext(BaseModel):
    target_date: date

    existing_events: List[ExistingEventContext]

    candidate_work_items: List[CandidateWorkItem]

    user_explicit_intent: bool

