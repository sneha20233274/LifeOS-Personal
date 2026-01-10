from my_agent.chatstate import ChatState
from my_agent.llm import evaluator_structured_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
def diet_evaluator_node(
    state: ChatState
) -> ChatState:
    """
    Evaluates the generated diet plan.
    """
    diet_plan = state["diet_plan"]
    evaluation_prompt = f"""
    Given the diet plan: {diet_plan},
    provide feedback on its effectiveness and safety.
    Suggest improvements if necessary.
    Finally, indicate whether the plan is approved (true/false).
    """

    messages = [
        SystemMessage(content="You are an expert evaluator of diet plans."),
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