from datetime import date, datetime, timedelta

from app.models.routine_event import RoutineEvent
from app.models.subtask import Subtask
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime, timedelta
from my_agent.chatstate import ChatState


def daily_context_builder_node(state: ChatState, config):
    # -------------------------------
    # SAFE CONFIG ACCESS
    # -------------------------------
    configurable = config.get("configurable", {})
    
    user_id = configurable.get("user_id")
    db = configurable.get("db")

    if not db:
        raise ValueError("Database session (db) not provided in config")

    # -------------------------------
    # GET TARGET DATE
    # -------------------------------
    decision = state["planning_decision"]
    target_date: date = decision.target_date

    # Convert date → datetime range
    start_dt = datetime.combine(target_date, datetime.min.time())
    end_dt = start_dt + timedelta(days=1)

    # ------------------------------------------------
    # 1. Fetch existing RoutineEvents (FIXED ✅)
    # ------------------------------------------------
    existing_events = (
        db.query(RoutineEvent)
        .filter(
            RoutineEvent.user_id == user_id,
            RoutineEvent.start_time >= start_dt,
            RoutineEvent.start_time < end_dt,
        )
        .all()
    )

    # Optional: serialize events (recommended for LLM)
    existing_events_serialized = [
        {
            "id": ev.id,
            "title": ev.title,
            "start_time": ev.start_time.isoformat(),
            "end_time": ev.end_time.isoformat() if ev.end_time else None,
            "locked": True,  # 🔥 important for planner
        }
        for ev in existing_events
    ]

    # ------------------------------------------------
    # 2. If schedule_only, stop here
    # ------------------------------------------------
    if decision.planning_mode == "schedule_only":
        return {
            "daily_context": {
                "target_date": target_date.isoformat(),
                "existing_events": existing_events_serialized,
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
        goal = db.query(Goal).get(task.goal_id) if task and task.goal_id else None

        # ---- priority signals ----
        goal_importance = goal.importance_level if goal else 0
        task_difficulty = task.difficulty if task else 0

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
                "task_id": task.task_id if task else None,
                "task_name": task.task_name if task else None,
                "difficulty": task_difficulty,
            },
            "goal": {
            "goal_id": goal.goal_id,
            "goal_name": goal.goal_name,
            "importance_level": goal_importance,
            "target_date": goal.target_date.isoformat() if goal.target_date else None,
          } if goal else None,
            "priority_score": priority_score,
        })

    # ------------------------------------------------
    # FINAL RETURN
    # ------------------------------------------------
    return {
        "daily_context": {
            "target_date": target_date.isoformat(),
            "existing_events": existing_events_serialized,
            "candidate_work_items": candidate_work_items,
            "user_explicit_intent": decision.planning_mode != "full_planning",
        }
    }