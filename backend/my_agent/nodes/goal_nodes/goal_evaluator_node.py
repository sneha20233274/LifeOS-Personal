
from my_agent.chatstate import ChatState
from my_agent.llm import evaluator_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def goal_evaluator_node(
    state: ChatState
) -> ChatState:
    """
    Evaluates the proposed routine.
    """
    routine = state["routine_tasks"]
    goal = state["structured_goal"]

    evaluation_prompt = f"""
    Given the goal: {goal} and the proposed routine: {routine},
    provide feedback on how well the routine aligns with the goal.
    Suggest improvements if necessary.
    Finally, indicate whether the routine is approved (true/false).
    """

    messages = [
        SystemMessage(content="You are an expert evaluator of routines."),
        HumanMessage(content=evaluation_prompt)
    ]
    print("Messages to evaluator LLM:", messages)
    llm_output = evaluator_structured_llm.invoke(messages)
    print("Evaluator LLM output:", llm_output)

    # Parse output (assuming simple text parsing for demo purposes)
    print(llm_output)
    feedback = llm_output.feedback
    approved = llm_output.approved

    new_state = {
        **state,
        "feedback": feedback,
        "approved": approved
    }

    return new_state