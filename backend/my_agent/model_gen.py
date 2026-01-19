from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from typing import Literal

from my_agent.chatstate import ChatState
from my_agent.checkpointer import checkpointer

# ---------------- INTENT ----------------
from my_agent.nodes.intent_resolver_node import intent_resolver_node

# ---------------- GOAL ----------------
from my_agent.nodes.goal_nodes.goal_prompt_builder_node import goal_prompt_builder_node
from my_agent.nodes.goal_nodes.routine_generator_node import routine_generator_node
from my_agent.nodes.goal_nodes.goal_evaluator_node import goal_evaluator_node
from my_agent.nodes.goal_nodes.goal_optimiser_node import goal_optimisor_node

# ---------------- FITNESS ----------------
from my_agent.nodes.fitness_nodes.fitness_planner_node import fitness_planer_node
from my_agent.nodes.fitness_nodes.fitness_planner_node2 import (
    weekly_focus_node,
    day_timeline_skeleton_node,
    timeslot_detail_node,
    weekly_routine_assembly_node,
)
from my_agent.nodes.fitness_nodes.fitness_evaluator_node import fitness_evaluator_node
from my_agent.nodes.fitness_nodes.fitness_optimiser_node import fitness_optimisor_node


# ---------------- DIET ----------------
from my_agent.nodes.diet_nodes.diet_planner_node import diet_planer_node
from my_agent.nodes.diet_nodes.diet_evaluator_node import diet_evaluator_node
from my_agent.nodes.diet_nodes.diet_optimisor_node import diet_optimisor_node

# ---------------- TASK ----------------
from my_agent.nodes.create_task_subtask.task_creator_node import task_creator_node
from my_agent.nodes.create_task_subtask.task_creator_optimisor_node import task_optimiser_node
from my_agent.nodes.create_task_subtask.task_creator_evaluator_node import task_evaluator_node

# ---------------- PROPOSAL ----------------
from my_agent.nodes.proposal_action_nodes.proposal_buider_node import proposal_builder_node
from my_agent.nodes.proposal_action_nodes.wait_for_approval_node import wait_for_approval_node
from my_agent.nodes.proposal_action_nodes.post_execution_reflect_node import post_execution_reflect_node

# ---------------- ACTIVITY ----------------
from my_agent.nodes.activity.activity_create_node import activity_create_node

# ---------------- ANALYTICS ----------------
from my_agent.nodes.analytics_node.aggregation_node import aggregation_node
from my_agent.nodes.analytics_node.analysis_node import analysis_node, tools_by_name


# ======================================================
# ROUTING HELPERS
# ======================================================

def conditional_decision(state: ChatState):
    if not state["approved"] and state["iteration"] < state["max_iterations"]:
        return "need_improvement"
    return "approved"

def conditonal_intent_resolver(state: ChatState):
    return state["intent"]

def execution_router(state: ChatState):
    return "execute" if state.get("requires_execution") else "no_execute"

def should_continue(state: ChatState) -> Literal["tool_node_analytics", "end"]:
    last_message = state["messages"][-1]
    return "tool_node_analytics" if last_message.tool_calls else "end"


def tool_node_analytics(state: ChatState, config: RunnableConfig):
    messages = []
    current_user_id = config.get("configurable", {}).get("user_id")
    if not current_user_id:
        raise ValueError("User ID missing")

    new_metrics, new_comparisons = {}, {}
    last_message = state["messages"][-1]

    for tool_call in last_message.tool_calls:
        tool_args = tool_call["args"]
        tool_args["user_id"] = current_user_id
        tool = tools_by_name[tool_call["name"]]
        output = tool.invoke(tool_args)

        messages.append(
            ToolMessage(
                content=str(output),
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            )
        )

        if isinstance(output, dict):
            if "productivity_score" in output:
                new_metrics.update(output)
            if "trend" in output:
                new_comparisons.update(output)

    return {
        "messages": messages,
        "metric_result": new_metrics,
        "comparison_result": new_comparisons,
    }


# ======================================================
# GRAPH
# ======================================================

graph = StateGraph(ChatState)

# ---------------- ADD NODES ----------------
graph.add_node("intent_resolver", intent_resolver_node)

# goal
graph.add_node("goal_prompt_builder_node", goal_prompt_builder_node)
graph.add_node("routine_generator_node", routine_generator_node)
graph.add_node("goal_evaluator_node", goal_evaluator_node)
graph.add_node("goal_optimisor_node", goal_optimisor_node)

# fitness
graph.add_node("fitness_planer", fitness_planer_node)
# ---------- FITNESS (NEW PIPELINE) ----------

graph.add_node("fitness_evaluator_node",fitness_evaluator_node)

graph.add_node("fitness_optimisor_node", fitness_optimisor_node)


# diet
graph.add_node("diet_planer", diet_planer_node)
graph.add_node("diet_evaluator_node", diet_evaluator_node)
graph.add_node("diet_optimisor_node", diet_optimisor_node)

# task
graph.add_node("task_creator_node", task_creator_node)
graph.add_node("task_optimiser_node", task_optimiser_node)
graph.add_node("task_evaluator_node", task_evaluator_node)

# proposal
graph.add_node("proposal_builder", proposal_builder_node)
graph.add_node("wait_for_approval", wait_for_approval_node)
graph.add_node("post_execution_reflect", post_execution_reflect_node)

# activity + analytics
graph.add_node("activity_create_node", activity_create_node)
graph.add_node("aggregation_node", aggregation_node)
graph.add_node("analysis_node", analysis_node)
graph.add_node("tool_node_analytics", tool_node_analytics)

# ---------------- EDGES ----------------

graph.add_edge(START, "intent_resolver")

graph.add_conditional_edges(
    "intent_resolver",
    conditonal_intent_resolver,
    {
        "fitness": "fitness_planer",
        "diet": "diet_planer",
        "goal": "goal_prompt_builder_node",
        "task": "task_creator_node",
        "activity_create": "activity_create_node",
        "analytics": "aggregation_node",
    },
)
# ---------- GOAL ----------
graph.add_edge("goal_prompt_builder_node", "routine_generator_node")
graph.add_edge("routine_generator_node", "goal_evaluator_node")
graph.add_conditional_edges(
    "goal_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "goal_optimisor_node",
        "approved": "proposal_builder",
    },
)
graph.add_edge("goal_optimisor_node", "goal_evaluator_node")

# ---------- FITNESS (UPDATED) ----------
graph.add_node("weekly_focus_node", weekly_focus_node)
graph.add_node("day_timeline_skeleton_node", day_timeline_skeleton_node)
graph.add_node("timeslot_detail_node", timeslot_detail_node)
graph.add_node("weekly_routine_assembly_node", weekly_routine_assembly_node)


graph.add_edge("fitness_planer", "weekly_focus_node")
graph.add_edge("weekly_focus_node", "day_timeline_skeleton_node")
graph.add_edge("day_timeline_skeleton_node", "timeslot_detail_node")
graph.add_edge("timeslot_detail_node", "weekly_routine_assembly_node")
graph.add_edge("weekly_routine_assembly_node", "fitness_evaluator_node")



graph.add_conditional_edges(
    "fitness_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "fitness_optimisor_node",
        "approved": "proposal_builder",
    },
)

graph.add_edge("fitness_optimisor_node", "fitness_evaluator_node")

# ---------- DIET ----------
graph.add_edge("diet_planer", "diet_evaluator_node")
graph.add_conditional_edges(
    "diet_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "diet_optimisor_node",
        "approved": "proposal_builder",
    },
)
graph.add_edge("diet_optimisor_node", "diet_evaluator_node")

# ---------- PROPOSAL / EXECUTION ----------
graph.add_conditional_edges(
    "proposal_builder",
    execution_router,
    {
        "execute": "wait_for_approval",
        "no_execute": END,
    },
)

graph.add_edge("wait_for_approval", "post_execution_reflect")
graph.add_edge("post_execution_reflect", END)

# ---------- TASK ----------
graph.add_edge("task_creator_node", "task_evaluator_node")
graph.add_conditional_edges(
    "task_evaluator_node",
    conditional_decision,
    {
        "need_improvement": "task_optimiser_node",
        "approved": "proposal_builder",
    },
)
graph.add_edge("task_optimiser_node", "task_evaluator_node")

# ---------- ACTIVITY ----------
graph.add_edge("activity_create_node", "proposal_builder")

# ---------- ANALYTICS ----------
graph.add_edge("aggregation_node", "analysis_node")
graph.add_conditional_edges(
    "analysis_node",
    should_continue,
    {
        "tool_node_analytics": "tool_node_analytics",
        "end": END,
    },
)
graph.add_edge("tool_node_analytics", "analysis_node")

# ---------------- COMPILE ----------------
chatbot = graph.compile(checkpointer=checkpointer)
if __name__ == "__main__":
    from pprint import pprint

    print("\n===== RUNNING FITNESS FLOW TEST =====\n")

    initial_state: ChatState = {
        "messages": [
            HumanMessage(
                content=(
                    "I want a muscle gain fitness routine. "
                    "I train in the morning from 9am to 10am. "
                    "Monday should be leg day, Tuesday push day, "
                    "Wednesday rest, Thursday pull day. "
                    "Include warmup, exercises with sets and reps, "
                    "breaks between sets, and cooldown."
                )
            )
        ],
        "intent": "fitness",          # VERY IMPORTANT
        "iteration": 0,
        "max_iterations": 2,
        "approved": False,
        "requires_execution": False   # prevents DB / proposal execution
    }

final_state = chatbot.invoke(
    initial_state,
    config={
        "configurable": {
            "user_id": 1,
            "thread_id": "fitness_test_thread_1"
        }
    }
)


print("\n===== FINAL STATE KEYS =====")
print(final_state.keys())

print("\n===== WEEKLY FITNESS ROUTINE =====")
if "weekly_routine" in final_state:
        pprint(final_state["weekly_routine"])
else:
        print("❌ weekly_routine not generated")

print("\n===== DONE =====\n")
