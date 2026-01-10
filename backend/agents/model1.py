import os
from datetime import date
from enum import Enum
from typing import TypedDict, Annotated, Dict, Any, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq

# 1. Configuration & Initialization
load_dotenv()

# Note: Ensure GROQ_API_KEY is set in your .env file
llm_model_main = "openai/gpt-oss-120b"
llm_model_goal = "llama-3.1-8b-instant"

# 2. Pydantic Schemas for Structured Output
class GoalCreate(BaseModel):
    goal_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    target_date: Optional[date] = None
    importance_level: int = Field(default=1, ge=1, le=5)
    motivations: Optional[List[str]] = None

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
    weight: int = 1
    deadline: Optional[date] = None
    depends_on_subtask_key: Optional[str] = None

class GeneratedTask(BaseModel):
    temp_task_key: str
    task_name: str
    description: Optional[str] = None
    difficulty: int = Field(ge=1, le=5)
    depends_on_task_key: Optional[str] = None
    subtasks: List[GeneratedSubtask]

class RoutineGenerationOutput(BaseModel):
    tasks: List[GeneratedTask]

class RoutineSuggestions(BaseModel):
    suggestions: List[str]

class RoutineLLMOutput(BaseModel):
    routine: RoutineGenerationOutput
    suggestions: RoutineSuggestions

# 3. State Definition
class ChatState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]
    intent: str
    structured_goal: Dict[str, Any]   # GoalCreate output
    routine_tasks: List[Dict[str, Any]]

# 4. LLM Setup
goal_prompt_llm = ChatGroq(model=llm_model_goal, temperature=0.1)
goal_prompt_structured_llm = goal_prompt_llm.with_structured_output(GoalCreate)

routine_llm = ChatGroq(model=llm_model_main, temperature=0.3)
routine_structured_llm = routine_llm.with_structured_output(RoutineLLMOutput)

# 5. System Prompts
GOAL_PROMPT_SYSTEM = """
You are a goal normalization engine.

Your task:
- Convert informal user input into a structured goal.

Rules:
- goal_name must be concise and specific
- description should expand what the user wants to achieve
- target_date:
  - infer ONLY if user explicitly mentions a time (e.g. "2022-12-25") 
  - use current time as reference if user mentions duration to evaluate target date
  - otherwise set it to null
- importance_level:
  - infer urgency (1 = casual, 5 = very important)
- motivations:
  - infer clear motivations if stated or obvious
  - otherwise null

Do NOT ask questions.
Do NOT add extra fields.
Return ONLY structured output.
"""

ROUTINE_SYSTEM_PROMPT = """
You are a routine generation engine.

Generate:
1. Tasks and subtasks ONLY in structured form
2. High-level suggestions for the user as text

Rules:
- Tasks must match Task + Subtask schema
- No IDs, no completion fields
- Use temporary keys for dependencies
"""

# 6. Node Functions
def goal_prompt_builder_node(state: ChatState) -> ChatState:
    """Converts user input into GoalCreate schema."""
    print("--- Entering Goal Builder Node ---")
    user_text = state["messages"][-1].content

    messages = [
        SystemMessage(content=GOAL_PROMPT_SYSTEM),
        HumanMessage(content=user_text),
    ]
    
    goal: GoalCreate = goal_prompt_structured_llm.invoke(messages)
    
    # Update state with structured goal
    new_state = {
        **state,
        "structured_goal": goal.model_dump()
    }

    confirmation = (
        "I’ve understood your goal as:\n\n"
        f"🎯 Goal: {goal.goal_name}\n"
        f"📝 Description: {goal.description or '—'}\n"
        f"📅 Target Date: {goal.target_date or 'Not specified'}\n"
        f"⭐ Importance Level: {goal.importance_level}/5\n"
    )

    if goal.motivations:
        confirmation += "💡 Motivations:\n"
        for m in goal.motivations:
            confirmation += f"• {m}\n"

    new_state["messages"] = [AIMessage(content=confirmation)]
    return new_state

def routine_generator_node(state: ChatState) -> ChatState:
    """Generates tasks, subtasks, and suggestions based on the goal."""
    print("--- Entering Routine Generator Node ---")
    # We use the previous AI confirmation or the structured goal as context
    goal_context = state["messages"][-1].content 

    messages = [
        SystemMessage(content=ROUTINE_SYSTEM_PROMPT),
        HumanMessage(content=goal_context)
    ]
    
    llm_output = routine_structured_llm.invoke(messages)
    
    new_state = {
        **state,
        "routine_tasks": [task.model_dump() for task in llm_output.routine.tasks]
    }

    suggestion_text = "\n".join(f"- {s}" for s in llm_output.suggestions.suggestions)
    
    new_state["messages"] = [
        AIMessage(content=f"Here are some suggestions to follow along with this routine:\n{suggestion_text}")
    ]

    return new_state

# 7. Graph Construction
workflow = StateGraph(ChatState)

workflow.add_node('goal_prompt_builder_node', goal_prompt_builder_node)
workflow.add_node('routine_generator_node', routine_generator_node)

workflow.add_edge(START, 'goal_prompt_builder_node')
workflow.add_edge('goal_prompt_builder_node', 'routine_generator_node')
workflow.add_edge('routine_generator_node', END)

chatbot = workflow.compile()

# 8. Execution Example
if __name__ == "__main__":
    initial_state = {
        'messages': [HumanMessage(content='i want to complete dsa from basics to advance level in 6 months')]
    }

    final_output = chatbot.invoke(initial_state)
    
    print("\n--- Final Chat History ---")
    for msg in final_output['messages']:
        role = "User" if isinstance(msg, HumanMessage) else "AI"
        print(f"{role}: {msg.content}\n")