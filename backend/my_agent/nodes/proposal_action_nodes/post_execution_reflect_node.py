from langchain_core.messages import SystemMessage
from my_agent.llm import base_llm as llm
from my_agent.chatstate import ChatState


def post_execution_reflect_node(state: ChatState):
    execution_result = state.get("execution_result")

    # Nothing to reflect on
    if not execution_result:
        return state

    system_prompt = f"""
You are a system reflection engine.

The system has just executed user-approved changes.

Execution result (JSON):
{execution_result}

Your task:
1. Clearly explain what changes were successfully applied.
2. Mention any actions that were skipped and why.
3. Briefly suggest what the user could do next (if relevant).

Be concise, factual, and helpful.
"""

    reflection_message = SystemMessage(content=system_prompt)

    response = llm.invoke(
        state["messages"] + [reflection_message]
    )

    # IMPORTANT: append, don't replace
    return {
        "messages": [response]
    }
