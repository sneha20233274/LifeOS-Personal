from pydantic import BaseModel, Field
from typing import List

from my_agent.schemas.task_subtasktype import GeneratedTask

class RoutineGenerationOutput(BaseModel):
    tasks: List[GeneratedTask]

class RoutineSuggestions(BaseModel):
    suggestions: List[str]
    
class RoutineLLMOutput(BaseModel):
    routine: RoutineGenerationOutput
    suggestions: RoutineSuggestions