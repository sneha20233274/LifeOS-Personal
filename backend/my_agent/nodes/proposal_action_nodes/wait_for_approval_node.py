from langgraph.types import interrupt
from my_agent.chatstate import ChatState
def wait_for_approval_node(state: ChatState):
    interrupt({
        "type": "HITL_APPROVAL",
        "proposals": state["proposals"],
        "message": "Approve or edit proposed changes"
    })
    return {}
