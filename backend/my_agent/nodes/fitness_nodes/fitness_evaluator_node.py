from my_agent.chatstate import ChatState
from my_agent.llm import evaluator_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def fitness_evalautor_node(
    state: ChatState
) -> ChatState:
    """
    Evaluates the generated fitness plan.
    """
    fitness_plan = state["fitness_plan"]
    evaluation_prompt = f"""
    Given the fitness plan: {fitness_plan},
    provide feedback on its effectiveness and safety.
    Suggest improvements if necessary.
    Finally, indicate whether the plan is approved (true/false).
    """

    messages = [
        SystemMessage(content="You are an expert evaluator of fitness plans."),
        HumanMessage(content=evaluation_prompt)
    ]
    
    llm_output = evaluator_structured_llm.invoke(messages)
   

    # Parse output (assuming simple text parsing for demo purposes)
  
    feedback = llm_output.feedback
    approved = llm_output.approved

    new_state = {
        **state,
        "feedback": feedback,
        "approved": approved
    }

    return new_state