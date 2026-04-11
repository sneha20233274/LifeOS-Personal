
from my_agent.chatstate import ChatState
from my_agent.llm import routine_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def goal_optimisor_node(
    state: ChatState
) -> ChatState:
    """
    Optimizes the routine based on evaluator feedback.
    """
    routine = state["routine_tasks"]
    feedback = state["feedback"]
    goal = state["structured_goal"]
    optimization_prompt = f"""
    You are a routine optimization engine.
    Given the routine: {routine} for the goal {goal} and the following feedback: {feedback},
    make necessary improvements to the routine.

    Rules:
    - Preserve the overall structure of the routine
    - Only modify tasks/subtasks where improvement is needed
    - Ensure all outputs strictly follow the schema

    CRITICAL RULES (STRICT):
    - deadline MUST be either:
    - a valid ISO date string (YYYY-MM-DD), OR
    - null
    - DO NOT use natural language deadlines like:
    - "weekly", "every Sunday", "daily", "twice per week"
    - If a task is recurring → set deadline = null

    - Keep tasks realistic and achievable
    - Maintain logical ordering of tasks

    - Subtasks:
    - must be actionable and clear
    - must belong to a task
    - avoid vague descriptions

    - priority:
    - must be numeric and consistent with importance

    - Do NOT:
    - add explanations
    - add extra fields

    Return ONLY structured output
    """

    messages = [
        SystemMessage(content="You are a routine optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]
    print("Messages to optimizer LLM:", messages)
    llm_output = routine_structured_llm.invoke(messages)
    print("Optimizer LLM output:", llm_output)
    iteration = state.get("iteration", 0)
    iteration += 1
    new_state = {
        **state,
        "routine_proposal": llm_output.routine.tasks,
        "iteration": iteration
    }

    return new_state