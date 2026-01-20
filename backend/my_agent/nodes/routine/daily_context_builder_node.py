from datetime import date
from app.models.routine_event import RoutineEvent
from app.models.subtask import Subtask
from app.models.task import Task
from app.models.goal import Goal

from my_agent.chatstate import ChatState
def daily_context_builder_node(state:ChatState,config):
    user_id = config["configurable"]["user_id"]
    
    db = config["configurable"]["db"]

    decision = state["planning_decision"]
    target_date: date = decision.target_date

    # ------------------------------------------------
    # 1. Fetch existing RoutineEvents (ALWAYS)
    # ------------------------------------------------
    existing_events = (
        db.query(RoutineEvent)
        .filter(
            RoutineEvent.user_id == user_id,
            RoutineEvent.start_time.cast(date) == target_date
        )
        .all()
    )

    # ------------------------------------------------
    # 2. If schedule_only, stop here
    # ------------------------------------------------
    if decision.planning_mode == "schedule_only":
        return {
            "daily_context": {
                "target_date": target_date,
                "existing_events": existing_events,
                "candidate_work_items": [],
                "user_explicit_intent": True,
            }
        }

    # ------------------------------------------------
    # 3. Fetch candidate subtasks
    # ------------------------------------------------
    subtasks = (
        db.query(Subtask)
        .filter(
            Subtask.user_id == user_id,
            Subtask.achieved == False
        )
        .all()
    )

    candidate_work_items = []

    for subtask in subtasks:
        task = db.query(Task).get(subtask.task_id)
        goal = db.query(Goal).get(task.goal_id) if task.goal_id else None

        # ---- priority signals ----
        goal_importance = goal.importance_level if goal else 0
        task_difficulty = task.difficulty

        urgency_bonus = 0
        if goal and goal.target_date:
            days_left = (goal.target_date - target_date).days
            urgency_bonus = max(0, 10 - days_left)

        priority_score = (
            goal_importance * 10
            + task_difficulty * 3
            + urgency_bonus
        )

        candidate_work_items.append({
            "subtask_id": subtask.subtask_id,
            "subtask_name": subtask.subtask_name,
            "subtask_type": subtask.subtask_type,
            "weight": subtask.weight,
            "task": {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "difficulty": task.difficulty,
            },
            "goal": {
                "goal_id": goal.goal_id,
                "goal_name": goal.goal_name,
                "importance_level": goal.importance_level,
                "target_date": goal.target_date,
            } if goal else None,
            "priority_score": priority_score,
        })

    return {
        "daily_context": {
            "target_date": target_date,
            "existing_events": existing_events,
            "candidate_work_items": candidate_work_items,
            "user_explicit_intent": decision.planning_mode != "full_planning",
        }
    }
