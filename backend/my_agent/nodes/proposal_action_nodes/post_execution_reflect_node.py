from langchain_core.messages import SystemMessage
from my_agent.llm import base_llm as llm
from my_agent.chatstate import ChatState

def post_execution_reflect_node(state: ChatState):
    if not state.get("execution_result"):
        return state

    msg = SystemMessage(
        content=f"Execution completed: {state['execution_result']}"
    )

    response = llm.invoke(state["messages"] + [msg])

    return {
        "messages": [response]
    }
