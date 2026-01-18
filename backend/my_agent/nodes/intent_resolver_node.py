from my_agent.chatstate import ChatState
from my_agent.llm import intent_resolver_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
 
def intent_resolver_node(
    state: ChatState
) -> ChatState:
    """
    Resolves user intent to determine if it's fitness or diet related.
    """
    user_text = state["messages"][-1].content
    
    intent_prompt = f"""
    Determine the user's intent from the following text: {user_text}.
    Is the user looking to update their fitness plan, diet plan, or something else?
    - If fitness related, respond with 'fitness'.
    - If diet related, respond with 'diet'.
    - If goal creation related, respond with 'goal'.
    - If activity logging creation respond with create 'activity_create' (activity logging is behabiour where user wants to save that he did something or he wants to same it as their activity)
    - If it is regarding creating task or subtask not related to fitness or diet, respond with 'task'.
    -If it is regarding analytics questions response with 'analytics' or some question requiring data or user activity information or productivity
    - Otherwise, respond with an empty string.
    """
    messages = [
        SystemMessage(content="You are an intent resolution engine."),
        HumanMessage(content=intent_prompt)
    ]

    llm_output = intent_resolver_llm.invoke(messages)
    print("Intent Resolver LLM output:", llm_output.intent.value)
    new_state = {
        **state,
        "intent": llm_output.intent.value
    }
    return new_state