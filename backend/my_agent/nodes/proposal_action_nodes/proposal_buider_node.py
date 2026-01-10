from my_agent.chatstate import ChatState
def proposal_builder_node(state: ChatState):
    proposals = []

    if state.get("structured_goal"):
        proposals.append({
            "action_type": "create_goal",
            "payload": state["structured_goal"]
        })

    if state.get("routine_tasks"):
        for task in state["routine_tasks"]:
            proposals.append({
                "action_type": "create_task",
                "payload": task
            })

    if state.get("fitness_plan"):
        proposals.append({
            "action_type": "update_fitness_plan",
            "payload": state["fitness_plan"]
        })

    if state.get("diet_plan"):
        proposals.append({
            "action_type": "update_diet_plan",
            "payload": state["diet_plan"]
        })

    return {
        "proposals": proposals,
        "requires_execution": len(proposals) > 0
    }
