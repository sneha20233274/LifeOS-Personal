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
        You are refining an existing task and subtask structure.

        User request:
        {user_request}

        Current tasks and subtasks:
        {tasks}

        Evaluator feedback:
        {feedback}

        Your objective:
        Improve the task and subtask structure based on the feedback while preserving the original intent.

        STRICT RULES (IMPORTANT):
        - Do NOT introduce goals, timelines, schedules, deadlines, dates, or progress tracking.
        - If a "deadline" field exists, it MUST be null.
        - NEVER add values like "Day 1", "Day 2", weeks, or relative time references.
        - Do NOT invent new high-level tasks unless explicitly required by the feedback.
        - Do NOT remove valid tasks or subtasks unless feedback explicitly says so.

        Structural guidelines:
        - Keep tasks aligned with the user request.
        - Tasks must represent clear scopes of work.
        - Subtasks must be concrete, executable actions.
        - Preserve dependencies unless feedback requires changes.
        - Keep names concise and descriptions precise.
        - Use neutral, instructional language.

        Output requirements:
        - Return the same structured format as the input.
        - Do not include commentary, explanations, or extra text.
        """

    messages = [
        SystemMessage(content="You are a task structure optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]

    llm_output = routine_structured_llm.invoke(messages)

    iteration = state.get("iteration", 0) + 1

    new_state = {
        **state,
        "routine_tasks": llm_output.routine.tasks,
        "iteration": iteration
    }

    return new_state
