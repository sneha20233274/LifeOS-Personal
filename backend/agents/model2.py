import os
from datetime import date
from enum import Enum
from typing import TypedDict, Annotated, Dict, Any, List, Optional

from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# ==========================================
# 1. DATA MODELS & SCHEMAS
# ==========================================

class GoalCreate(BaseModel):
    goal_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    start_date: date = Field(default_factory=date.today)
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

class EvaluatorOutput(BaseModel):
    feedback: str
    approved: bool

# ==========================================
# 2. PROMPTS
# ==========================================

GOAL_PROMPT_SYSTEM = """
You are a goal normalization engine.

Your task:
- Convert informal user input into a structured goal.

Rules:
- goal_name must be concise and specific
- description should expand what the user wants to achieve
- start_date is always today unless user specified that i want to start from a date in future
- target_date:
  - infer ONLY if user explicitly mentions a time (e.g. "2022-12-25") use current time as reference if user mentions duration to evaluate target date
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

# ==========================================
# 3. LLM INITIALIZATION
# ==========================================

routine_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)
routine_structured_llm = routine_llm.with_structured_output(
    RoutineLLMOutput
)

goal_prompt_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1
)
goal_prompt_structured_llm = goal_prompt_llm.with_structured_output(
    GoalCreate
)

evaluator_llm = ChatGroq(
    model="openai/gpt-oss-120b"
)
evaluator_structured_llm = evaluator_llm.with_structured_output(
    EvaluatorOutput
)

# ==========================================
# 4. STATE & NODES
# ==========================================

class ChatState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]
    intent: str
    structured_goal: Dict[str, Any]
    routine_tasks: List[Dict[str, Any]]
    feedback: str
    approved: bool
    iteration: int
    max_iterations: int

def goal_prompt_builder_node(state: ChatState) -> ChatState:
    print("Routine generator node input state")
    user_text = state["messages"][-1].content
    messages = [
        SystemMessage(content=GOAL_PROMPT_SYSTEM),
        HumanMessage(content=user_text),
    ]
    goal: GoalCreate = goal_prompt_structured_llm.invoke(messages)
    
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
    goal = state["messages"][-1].content
    messages = [
        SystemMessage(content=ROUTINE_SYSTEM_PROMPT),
        HumanMessage(content=goal)
    ]
    llm_output = routine_structured_llm.invoke(messages)
    
    new_state = {
        **state,
        "routine_tasks": llm_output.routine.tasks
    }

    suggestion_text = "\n".join(
        f"- {s}" for s in llm_output.suggestions.suggestions
    )

    new_state["messages"] = [
        AIMessage(
            content=f"Here are some suggestions to follow along with this routine:\n{suggestion_text}"
        )
    ]
    return new_state

def evaluator_node(state: ChatState) -> ChatState:
    routine = state["routine_tasks"]
    goal = state["structured_goal"]
    evaluation_prompt = f"""
    Given the goal: {goal} and the proposed routine: {routine},
    provide feedback on how well the routine aligns with the goal.
    Suggest improvements if necessary.
    Finally, indicate whether the routine is approved (true/false).
    """
    messages = [
        SystemMessage(content="You are an expert evaluator of routines."),
        HumanMessage(content=evaluation_prompt)
    ]
    llm_output = evaluator_structured_llm.invoke(messages)
    
    return {
        **state,
        "feedback": llm_output.feedback,
        "approved": llm_output.approved
    }

def optimisor_node(state: ChatState) -> ChatState:
    # Note: 'routine_proposal' was used in notebook instead of 'routine_tasks' here
    routine = state.get("routine_proposal", []) 
    feedback = state["feedback"]
    goal = state["structured_goal"]
    optimization_prompt = f"""
    Given the routine: {routine} for the goal {goal} and the following feedback: {feedback},
    make necessary improvements to the routine.
    """
    messages = [
        SystemMessage(content="You are a routine optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]
    llm_output = routine_structured_llm.invoke(messages)
    iteration = state.get("iteration", 0) + 1
    
    return {
        **state,
        "routine_proposal": llm_output.routine.tasks,
        "iteration": iteration
    }

def conditional_decision(state: ChatState):
    if state.get('approved') == False and state.get('iteration', 0) < state.get('max_iterations', 1):
        return 'need_improvement'
    return 'approved'

# ==========================================
# 5. GRAPH CONSTRUCTION
# ==========================================

graph = StateGraph(ChatState)

graph.add_node('routine_generator_node', routine_generator_node)
graph.add_node('goal_prompt_builder_node', goal_prompt_builder_node)
graph.add_node('evaluator_node', evaluator_node)
graph.add_node('optimisor_node', optimisor_node)

graph.add_edge(START, 'goal_prompt_builder_node')
graph.add_edge('goal_prompt_builder_node', 'routine_generator_node')
graph.add_edge('routine_generator_node', 'evaluator_node')
graph.add_conditional_edges(
    'evaluator_node',
    conditional_decision,
    {'need_improvement': 'optimisor_node', 'approved': END}
)
graph.add_edge('optimisor_node', 'evaluator_node')

chatbot = graph.compile()

# ==========================================
# 6. EXECUTION & OUTPUT PRINTS
# ==========================================

if __name__ == "__main__":
    initial_input = {
        "messages": [HumanMessage(content="I want to master DSA in 6 months")],
        "iteration": 0,
        "max_iterations": 2
    }
    
    print("\n🚀 Initializing LifeOS Agent...")
    
    final_state = chatbot.invoke(initial_input)
    print(final_state)