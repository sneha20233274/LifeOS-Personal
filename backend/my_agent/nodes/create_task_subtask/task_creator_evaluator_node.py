from my_agent.chatstate import ChatState
from my_agent.llm import evaluator_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage


def task_evaluator_node(state: ChatState) -> ChatState:
    """
    Evaluates generated tasks and subtasks against the user's request.
    """

    user_request =  state["messages"][-1].content
    print("User request for evaluation:", user_request)
    tasks = state["routine_tasks"]  # tasks + subtasks structure

    evaluation_prompt = f"""
    User request:
    {user_request}

    Generated tasks and subtasks:
    {tasks}

    Evaluate the quality of this task decomposition.

    Evaluation criteria:
    - Tasks should represent clear scopes of work.
    - Subtasks should be concrete, actionable, and executable.
    - The decomposition should match the user's request.
    - Avoid unnecessary or missing subtasks.

    Provide concise feedback.
    Finally, indicate whether the decomposition is approved (true/false).
    """

    messages = [
        SystemMessage(content="You are an expert evaluator of task and subtask structures."),
        HumanMessage(content=evaluation_prompt)
    ]

    llm_output = evaluator_structured_llm.invoke(messages)

    new_state = {
        **state,
        "feedback": llm_output.feedback,
        "approved": llm_output.approved
    }

    return new_state
