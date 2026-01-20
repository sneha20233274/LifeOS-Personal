from my_agent.chatstate import ChatState
from app.utils.date_corruption_catch_helper import assert_deadline_type
def proposal_builder_node(state: ChatState):
    proposals = []

    # ---------------------------
    # 1️⃣ Goal proposal
    # ---------------------------
    if state.get("structured_goal"):
        proposals.append({
            "action_type": "create_goal",
            "payload": state["structured_goal"]
        })

    # ---------------------------
    # 2️⃣ Task + Subtask proposals
    # ---------------------------
    if state.get("routine_tasks"):
        for task in state["routine_tasks"]:
            task_key = task.temp_task_key

            # ---- Task proposal ----
            proposals.append({
                "action_type": "create_task",
                "payload": {
                    "task_name": task.task_name,
                    "description": task.description,
                    "difficulty": task.difficulty,
                    "temp_task_key": task_key, 
                    "depends_on_task_key":task.depends_on_task_key # 🔑 used by apply_dependencies
                }
            })

            # ---- Subtask proposals ----
            for subtask in task.subtasks:
                

                proposals.append({
                    "action_type": "create_subtask",
                    "payload": {
                        "subtask_name": subtask.subtask_name,
                        "subtask_type": subtask.subtask_type,
                        "target_value": subtask.target_value,
                        "weight": subtask.weight,
                        "deadline": subtask.deadline,
                        # 🔥 THIS IS WHAT YOU ASKED FOR
                        "depends_on_task_key": task_key,
                        "depends_on_subtask_key":subtask.depends_on_subtask_key,

                        # optional (if you already support this)
                        "temp_subtask_key": subtask.temp_subtask_key,
                    }
                })
    if state.get("activity_create"):
        for activity in state["activity_create"]:
            proposals.append({
                "action_type": "log_activity",
                "payload": {
                    "activity_name": activity.activity_name,
                    "activity_description": activity.activity_description,
                    "start_ts": activity.start_ts,
                    "end_ts": activity.end_ts,
                    "duration_minutes": activity.duration_minutes,
                    "summary_category": activity.summary_category,
                    "criteria_ids": activity.criteria_ids,
                }
            })       
    
    if state.get("weekly_routine"):
        proposals.append({
            "action_type": "create_weekly_fitness_routine",
            "payload": state["weekly_routine"]
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
