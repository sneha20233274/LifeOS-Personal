from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from my_agent.chatstate import ChatState
from langchain_core.messages import HumanMessage, ToolMessage
from my_agent.checkpointer import checkpointer
from langchain_core.runnables import RunnableConfig
from typing import Literal


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

from my_agent.nodes.create_task_subtask.task_creator_node import task_creator_node
from my_agent.nodes.create_task_subtask.task_creator_optimisor_node import task_optimiser_node
from my_agent.nodes.create_task_subtask.task_creator_evaluator_node import task_evaluator_node

from my_agent.nodes.activity.activity_create_node import activity_create_node
from my_agent.nodes.analytics_node.aggregation_node import aggregation_node
from my_agent.nodes.analytics_node.analysis_node import analysis_node,tools_by_name

def conditional_decision(state: ChatState):
    if state['approved'] == False and state['iteration'] < state['max_iterations']:
        return 'need_improvement'
    return 'approved'

def conditonal_intent_resolver(state: ChatState):
    return state["intent"]

def execution_router(state: ChatState):
    return "execute" if state.get("requires_execution") else "no_execute"

def should_continue(state: ChatState) -> Literal["tool_node_analytics", "end"]:
    """Decide if we should run tools or end."""
    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, route to the tool node
    if last_message.tool_calls:
        return "tool_node_analytics"

    # Otherwise, stop
    return "end"

def tool_node_analytics(state: ChatState,config : RunnableConfig):
    """Executes tools. Returns ONLY new data (deltas). State handles the merging."""
    messages = []
    configuration = config.get("configurable", {})
    current_user_id = configuration.get("user_id")

    if not current_user_id:
        raise ValueError("User ID missing from configuration!")
    
    # Empty dicts to store ONLY new data found in this turn
    new_metrics = {}
    new_comparisons = {}

    last_message = state["messages"][-1]

    for tool_call in last_message.tool_calls:

        tool_args = tool_call["args"]
        tool_args["user_id"] = current_user_id
        tool = tools_by_name[tool_call["name"]]
        
        # Execute tool
        output = tool.invoke(tool_call["args"])
        
        # Create ToolMessage
        messages.append(ToolMessage(
            content=str(output), 
            tool_call_id=tool_call["id"],
            name=tool_call["name"]
        ))

        # --- OPTIMIZED LOGIC ---
        # Just grab the new data. No need to read `state` or merge manually.
        if isinstance(output, dict):
            if "productivity_score" in output or "leisure_ratio" in output:
                new_metrics.update(output)
            
            if "trend" in output:
                new_comparisons.update(output)

    return {
        "messages": messages,             # add_messages will append these
        "metric_result": new_metrics,     # update_dict will merge this into existing state
        "comparison_result": new_comparisons # update_dict will merge this too
    }


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

#create task
graph.add_node('task_creator_node', task_creator_node)
graph.add_node('task_optimiser_node', task_optimiser_node)
graph.add_node('task_evaluator_node', task_evaluator_node)
#activity
graph.add_node('activity_create_node',activity_create_node)
#analytics
graph.add_node('aggregation_node',aggregation_node)
graph.add_node('analysis_node',analysis_node)
graph.add_node('tool_node_analytics', tool_node_analytics)


graph.add_edge(START , 'intent_resolver')
graph.add_conditional_edges('intent_resolver', conditonal_intent_resolver,
{
  'fitness': 'fitness_planer',
  'diet': 'diet_planer',
  'goal': 'goal_prompt_builder_node',
  'task': 'task_creator_node',
  'activity_create': 'activity_create_node',
  'analytics':'aggregation_node'
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

graph.add_edge('task_creator_node', 'task_evaluator_node')
graph.add_conditional_edges(
    "task_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "task_optimiser_node",
        "approved": "proposal_builder"
    }
)
graph.add_edge('task_optimiser_node','task_evaluator_node')

graph.add_edge('activity_create_node','proposal_builder')

graph.add_edge('aggregation_node','analysis_node')
graph.add_conditional_edges(
    "analysis_node",
    should_continue,
    {
        "tool_node_analytics": "tool_node_analytics", 
        "end": END
    }
)

graph.add_edge('tool_node_analytics','analysis_node')
chatbot = graph.compile(
    checkpointer=checkpointer
)



if __name__ == "__main__":
  initial_state = {
      'messages': [HumanMessage(content='master dsa , cp and prepare for google under 6 months')],
      "iteration": 0,
      "max_iterations": 3
  }

  chatbot.invoke(initial_state)