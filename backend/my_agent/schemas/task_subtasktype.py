from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum
class SubtaskType(str, Enum):
    checkbox = "checkbox"
    count = "count"
    duration = "duration"
    score = "score"


class GeneratedSubtask(BaseModel):
    temp_subtask_key: str

    subtask_name: str
    subtask_type: SubtaskType

    target_value: Optional[float] = None
    weight: float = 1
    deadline: Optional[date] = None

    depends_on_subtask_key: Optional[str] = None
    


class GeneratedTask(BaseModel):
    temp_task_key: str

    task_name: str
    description: Optional[str] = None
    difficulty: int = Field(ge=1, le=5)

    depends_on_task_key: Optional[str] = None
    subtasks: List[GeneratedSubtask]



