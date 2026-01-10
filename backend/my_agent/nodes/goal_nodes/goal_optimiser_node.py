
from my_agent.chatstate import ChatState
from my_agent.llm import routine_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def goal_optimisor_node(
    state: ChatState
) -> ChatState:
    """
    Optimizes the routine based on evaluator feedback.
    """
    routine = state["routine_tasks"]
    feedback = state["feedback"]
    goal = state["structured_goal"]
    optimization_prompt = f"""
    Given the routine: {routine} for the goal {goal} and the following feedback: {feedback},
    make necessary improvements to the routine.
    """

    messages = [
        SystemMessage(content="You are a routine optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]
    print("Messages to optimizer LLM:", messages)
    llm_output = routine_structured_llm.invoke(messages)
    print("Optimizer LLM output:", llm_output)
    iteration = state.get("iteration", 0)
    iteration += 1
    new_state = {
        **state,
        "routine_proposal": llm_output.routine.tasks,
        "iteration": iteration
    }

    return new_state