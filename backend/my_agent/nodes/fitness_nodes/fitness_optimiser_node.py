from my_agent.chatstate import ChatState
from my_agent.llm import structured_fitness_planer_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def fitness_optimisor_node(
    state: ChatState
) -> ChatState:
    """
    Optimizes the fitness plan based on evaluator feedback.
    """
    fitness_plan = state["fitness_plan"]
    feedback = state["feedback"]
    optimization_prompt = f"""
    Given the fitness plan: {fitness_plan} and the following feedback: {feedback},
    make necessary improvements to the fitness plan.
    """

    messages = [
        SystemMessage(content="You are a fitness plan optimization engine."),
        HumanMessage(content=optimization_prompt)
    ]
    
    llm_output = structured_fitness_planer_llm.invoke(messages)
   
    iteration = state.get("iteration", 0)
    iteration += 1
    new_state = {
        **state,
        "fitness_plan": llm_output.model_dump(),
        "iteration": iteration
    }

    return new_state