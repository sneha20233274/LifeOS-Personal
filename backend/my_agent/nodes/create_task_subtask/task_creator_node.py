from my_agent.chatstate import ChatState
from my_agent.llm import routine_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def task_creator_node(
    state: ChatState
) -> ChatState:
    """
    Creates a task based on user intent.
    """
    user_text = state["messages"][-1].content

    task_prompt = f"""
      You are a task decomposition engine for a study-focused system.

      User request:
      "{user_text}"

      Your responsibilities:
      - Identify one or more meaningful tasks implied by the request.
      - If user says to create subtasks make tasks and create a single subtask under that task
      - For each task, break it down into clear, concrete subtasks.
      - Work only at the Task and Subtask level (no goals).

      Guidelines:
      - Tasks represent scopes of work.
      - Subtasks represent executable actions that can be completed in a single focused session.
      - If the request is already a concrete action, create a single task with a single subtask.
      - Keep names concise and descriptions precise.
      - Do not invent unnecessary hierarchy.

      Constraints:
      - Do not include IDs, timestamps, progress, dependencies, or scheduling.
      - Do not add motivational or conversational text.
      - Use neutral, instructional language.

      Optional:
      - You may include brief high-level suggestions if they add value, separate from the structure.
      """

    messages = [
        SystemMessage(content="You are a task decomposition engine for a study-focused system."),
        HumanMessage(content=task_prompt)
    ]
    print("Messages to task creator LLM:", messages)
    llm_output = routine_structured_llm.invoke(messages)
    print("Task Creator LLM output:", llm_output)

    # Parse output (assuming simple text parsing for demo purposes)
   

    new_state = {
        **state,
        "routine_tasks": llm_output.routine.tasks
    }

    return new_state