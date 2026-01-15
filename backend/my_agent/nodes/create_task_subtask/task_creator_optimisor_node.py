from my_agent.chatstate import ChatState
from my_agent.llm import routine_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage


def task_optimiser_node(state: ChatState) -> ChatState:
    """
    Optimizes generated tasks and subtasks based on evaluator feedback.
    """

    user_request =  state["messages"][-1].content
    tasks = state["routine_tasks"]
    feedback = state["feedback"]

    optimization_prompt = f"""
    User request:
    {user_request}

    Current tasks and subtasks:
    {tasks}

    Evaluator feedback:
    {feedback}

    Improve the task and subtask structure based on the feedback.

    Guidelines:
    - Keep tasks aligned with the user request.
    - Ensure tasks represent clear scopes.
    - Ensure subtasks are concrete and actionable.
    - Do not introduce goals, timelines, or progress tracking.
    - Do not add unrelated tasks.
    """

    messages = [
        SystemMessage(content="You are a task structure optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]

    llm_output = routine_structured_llm.invoke(messages)

    iteration = state.get("iteration", 0) + 1

    new_state = {
        **state,
        "routine_tasks": llm_output.tasks,
        "iteration": iteration
    }

    return new_state
