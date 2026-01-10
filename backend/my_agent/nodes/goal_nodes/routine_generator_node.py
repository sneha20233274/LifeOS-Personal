from my_agent.chatstate import ChatState
from my_agent.llm import routine_structured_llm
from my_agent.prompts.routine_system_prompt import ROUTINE_SYSTEM_PROMPT   
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def routine_generator_node(
    state: ChatState
) -> ChatState:
    
    goal = state["messages"][-1].content  # user goal text

    messages = [
        SystemMessage(content=ROUTINE_SYSTEM_PROMPT),
        HumanMessage(content=goal)
    ]
    print("Messages to routine LLM:", messages)
    llm_output = routine_structured_llm.invoke(messages)
    print("Routine LLM output:", llm_output)
    # 1️⃣ Structured routine → state
    new_state = {
        **state,
        "routine_tasks": llm_output.routine.tasks
    }

    # 2️⃣ Suggestions → chat message
    suggestion_text = "\n".join(
        f"- {s}" for s in llm_output.suggestions.suggestions
    )

    new_state["messages"] = [
        AIMessage(
            content=f"Here are some suggestions to follow along with this routine:\n{suggestion_text}"
        )
    ]

    return new_state