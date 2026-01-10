from my_agent.chatstate import ChatState
from my_agent.llm import diet_planer_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def diet_optimisor_node(
    state: ChatState
) -> ChatState:
    """
    Optimizes the diet plan based on evaluator feedback.
    """
    diet_plan = state["diet_plan"]
    feedback = state["feedback"]
    optimization_prompt = f"""
    Given the diet plan: {diet_plan} and the following feedback: {feedback},
    make necessary improvements to the diet plan.
    """

    messages = [
        SystemMessage(content="You are a diet plan optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]
    
    llm_output = diet_planer_llm.invoke(messages)
   
    iteration = state.get("iteration", 0)
    iteration += 1
    new_state = {
        **state,
        "diet_plan": llm_output.model_dump(),
        "iteration": iteration
    }

    return new_state