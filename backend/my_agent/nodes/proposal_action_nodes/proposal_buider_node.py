from my_agent.chatstate import ChatState


def to_dict(obj):
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return {}


def proposal_builder_node(state: ChatState):
    proposals = []

    # ---------------------------
    # 1️⃣ Goal proposal
    # ---------------------------
    if state.get("structured_goal"):
        proposals.append({
            "action_type": "create_goal",
            "payload": to_dict(state["structured_goal"])
        })

    # ---------------------------
    # 2️⃣ Task + Subtask proposals
    # ---------------------------
    if state.get("routine_tasks"):
        for task in state["routine_tasks"]:
            task = to_dict(task)

            task_key = task.get("temp_task_key")

            proposals.append({
                "action_type": "create_task",
                "payload": {
                    "task_name": task.get("task_name"),
                    "description": task.get("description"),
                    "difficulty": task.get("difficulty"),
                    "temp_task_key": task_key,
                    "depends_on_task_key": task.get("depends_on_task_key"),
                }
            })

            # ---- Subtasks ----
            for subtask in task.get("subtasks", []):
                subtask = to_dict(subtask)

                proposals.append({
                    "action_type": "create_subtask",
                    "payload": {
                        "subtask_name": subtask.get("subtask_name"),
                        "subtask_type": subtask.get("subtask_type"),
                        "target_value": subtask.get("target_value"),
                        "weight": subtask.get("weight"),
                        "deadline": subtask.get("deadline"),
                        "depends_on_task_key": task_key,
                        "depends_on_subtask_key": subtask.get("depends_on_subtask_key"),
                        "temp_subtask_key": subtask.get("temp_subtask_key"),
                    }
                })

    # ---------------------------
    # 3️⃣ Routine Events
    # ---------------------------
    if state.get("routine_structure"):
        routine = to_dict(state.get("routine_structure"))
        events = routine.get("events", [])

        for event in events:
            event = to_dict(event)

            proposals.append({
                "action_type": "schedule_routine_event",
                "payload": {
                    "temp_event_key": event.get("temp_event_key"),
                    "title": event.get("title"),
                    "description": event.get("description"),
                    "start_time": event.get("start_time"),
                    "end_time": event.get("end_time"),
                    "is_all_day": event.get("is_all_day"),
                    "category": event.get("category"),
                    "priority": event.get("priority"),
                    "location_or_link": event.get("location_or_link"),
                    "source": event.get("source"),
                }
            })

    # ---------------------------
    # 4️⃣ Activity logs
    # ---------------------------
    if state.get("activity_create"):
        for activity in state["activity_create"]:
            activity = to_dict(activity)

            proposals.append({
                "action_type": "log_activity",
                "payload": {
                    "activity_name": activity.get("activity_name"),
                    "activity_description": activity.get("activity_description"),
                    "start_ts": activity.get("start_ts"),
                    "end_ts": activity.get("end_ts"),
                    "duration_minutes": activity.get("duration_minutes"),
                    "summary_category": activity.get("summary_category"),
                    "criteria_ids": activity.get("criteria_ids"),
                }
            })

    # ---------------------------
    # 5️⃣ Weekly routine
    # ---------------------------
    if state.get("weekly_routine"):
        proposals.append({
            "action_type": "create_weekly_fitness_routine",
            "payload": to_dict(state["weekly_routine"])
        })

    # ---------------------------
    # 6️⃣ Diet plan
    # ---------------------------
    if state.get("diet_plan"):
        proposals.append({
            "action_type": "update_diet_plan",
            "payload": to_dict(state["diet_plan"])
        })

    return {
        **state,
        "proposals": proposals,
        "requires_execution": len(proposals) > 0
    }