from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from my_agent.chatstate import ChatState
from langchain_core.messages import HumanMessage





from my_agent.nodes.goal_nodes.goal_prompt_builder_node import goal_prompt_builder_node
from my_agent.nodes.goal_nodes.routine_generator_node import routine_generator_node
from my_agent.nodes.goal_nodes.goal_evaluator_node import goal_evaluator_node
from my_agent.nodes.goal_nodes.goal_optimiser_node import goal_optimisor_node
from my_agent.nodes.intent_resolver_node import intent_resolver_node
from my_agent.nodes.fitness_nodes.fitness_planner_node import fitness_planer_node
from my_agent.nodes.fitness_nodes.fitness_evaluator_node import fitness_evalautor_node
from my_agent.nodes.fitness_nodes.fitness_optimiser_node import fitness_optimisor_node
from my_agent.nodes.diet_nodes.diet_planner_node import diet_planer_node
from my_agent.nodes.diet_nodes.diet_evaluator_node import diet_evaluator_node
from my_agent.nodes.diet_nodes.diet_optimisor_node import diet_optimisor_node
from my_agent.nodes.proposal_action_nodes.proposal_buider_node import proposal_builder_node
from my_agent.nodes.proposal_action_nodes.wait_for_approval_node import wait_for_approval_node
from my_agent.nodes.proposal_action_nodes.post_execution_reflect_node import post_execution_reflect_node






def conditional_decision(state: ChatState):
    if state['approved'] == False and state['iteration'] < state['max_iterations']:
        return 'need_improvement'
    return 'approved'

def conditonal_intent_resolver(state: ChatState):
    return state["intent"]

def execution_router(state: ChatState):
    return "execute" if state.get("requires_execution") else "no_execute"

graph = StateGraph(ChatState)

# add nodes
graph.add_node('routine_generator_node', routine_generator_node)
graph.add_node('goal_prompt_builder_node', goal_prompt_builder_node)
graph.add_node('goal_evaluator_node', goal_evaluator_node)
graph.add_node('goal_optimisor_node', goal_optimisor_node)
graph.add_node('intent_resolver', intent_resolver_node)
graph.add_node('fitness_planer', fitness_planer_node)
graph.add_node('fitness_evalautor_node', fitness_evalautor_node)
graph.add_node('fitness_optimisor_node', fitness_optimisor_node)
graph.add_node('diet_planer', diet_planer_node)
graph.add_node('diet_evaluator_node', diet_evaluator_node)
graph.add_node('diet_optimisor_node', diet_optimisor_node)
graph.add_node("proposal_builder", proposal_builder_node)
graph.add_node("wait_for_approval", wait_for_approval_node)
graph.add_node("post_execution_reflect", post_execution_reflect_node)



graph.add_edge(START , 'intent_resolver')
graph.add_conditional_edges('intent_resolver', conditonal_intent_resolver,
{
  'fitness': 'fitness_planer',
  'diet': 'diet_planer',
  'goal': 'goal_prompt_builder_node'
})
graph.add_edge('goal_prompt_builder_node', 'routine_generator_node')
graph.add_edge('routine_generator_node', 'goal_evaluator_node')
graph.add_conditional_edges(
    "goal_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "goal_optimisor_node",
        "approved": "proposal_builder"
    }
)

graph.add_edge('goal_optimisor_node', 'goal_evaluator_node')

graph.add_edge('fitness_planer', 'fitness_evalautor_node')

graph.add_conditional_edges(
    "fitness_evalautor_node",
    conditional_decision,
    {
        "need_improvement": "fitness_optimisor_node",
        "approved": "proposal_builder"
    }
)

graph.add_edge('fitness_optimisor_node', 'fitness_evalautor_node')
graph.add_edge('diet_planer', 'diet_evaluator_node')

graph.add_conditional_edges(
    "diet_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "diet_optimisor_node",
        "approved": "proposal_builder"
    }
)

graph.add_edge('diet_optimisor_node', 'diet_evaluator_node')

graph.add_conditional_edges(
    "proposal_builder",
    execution_router,
    {
        "execute": "wait_for_approval",
        "no_execute": END
    }
)

graph.add_edge("wait_for_approval", "post_execution_reflect")
graph.add_edge("post_execution_reflect", END)

chatbot = graph.compile()


if __name__ == "__main__":
  initial_state = {
      'messages': [HumanMessage(content='master dsa , cp and prepare for google under 6 months')],
      "iteration": 0,
      "max_iterations": 3
  }

  chatbot.invoke(initial_state)