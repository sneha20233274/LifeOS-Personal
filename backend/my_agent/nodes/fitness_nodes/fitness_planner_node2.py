from my_agent.chatstate import ChatState
from langchain_core.messages import SystemMessage, HumanMessage
from my_agent.llm import weekly_focus_llm

def weekly_focus_node(state: ChatState) -> ChatState:
    plan = state["fitness_plan"]

    prompt = f"""
You are assigning a weekly training focus.

Rules:
- Assign EXACTLY one focus per day
- Use recovery on rest days
- Follow the user's preferences if mentioned
- Be realistic given the weekly frequency

Fitness Plan:
{plan}
"""

    messages = [
        SystemMessage(content="You output only structured data."),
        HumanMessage(content=prompt)
    ]

    # ✅ Structured output
    weekly_focus_model = weekly_focus_llm.invoke(messages)

    return {
        **state,
        "weekly_focus": weekly_focus_model.model_dump()
    }



from my_agent.llm import day_timeline_llm


def day_timeline_skeleton_node(state: ChatState) -> ChatState:
    plan = state["fitness_plan"]
    weekly_focus = state["weekly_focus"]

    day_timelines: dict = {}

    for day, focus in weekly_focus.items():
        prompt = f"""
Create a workout timeline for {day}.

Focus: {focus}

Rules:
- Morning session
- Include warmup and cooldown
- Include at least one exercise block
- Reasonable breaks
"""

        messages = [
            SystemMessage(content="You output structured timeline blocks."),
            HumanMessage(content=prompt),
        ]

        # ✅ Structured output
        skeleton = day_timeline_llm.invoke(messages)

        # ✅ Convert blocks → dict with HH:MM-HH:MM keys
        timeline = {}
        for b in skeleton.blocks:
            key = f"{b.start}-{b.end}"
            timeline[key] = {
                "block_type": b.block_type,
                "category": b.category,
            }

        day_timelines[day] = timeline

    return {
        **state,
        "day_timelines": day_timelines
    }

from my_agent.chatstate import ChatState
from my_agent.llm import (
    strength_detail_llm,
    cardio_detail_llm,
    mobility_detail_llm,
)


def timeslot_detail_node(state: ChatState) -> ChatState:
    """
    Fills structured details for each timeline block.
    """
    day_timelines = state["day_timelines"]
    weekly_focus = state["weekly_focus"]

    for day, timeline in day_timelines.items():
        focus = weekly_focus[day]

        for _, block in timeline.items():
            category = block["category"]

            if category == "strength":
                detail = strength_detail_llm.invoke(
                    f"Generate ONE strength exercise for {focus}"
                )
                block["details"] = detail.model_dump()

            elif category == "cardio":
                detail = cardio_detail_llm.invoke(
                    f"Generate ONE cardio activity appropriate for {focus}"
                )
                block["details"] = detail.model_dump()

            elif category == "mobility":
                detail = mobility_detail_llm.invoke(
                    "Generate ONE mobility drill for warmup or cooldown"
                )
                block["details"] = detail.model_dump()

            else:
                # break / rest
                block["details"] = None

    return state



from my_agent.schemas.fitness import WeeklyFitnessRoutine
from datetime import datetime
import uuid


def weekly_routine_assembly_node(state: ChatState) -> ChatState:
    plan = state["fitness_plan"]
    weekly_focus = state["weekly_focus"]
    day_timelines = state["day_timelines"]

    schedule = {}

    for day, timeline in day_timelines.items():
        schedule[day] = {
            "day_label": day.title(),
            "focus": weekly_focus[day],
            "timeline": timeline,
        }

    routine_data = {
        "routine_id": str(uuid.uuid4()),
        "routine_name": (
            f"{plan['goal'].replace('_', ' ').title()} "
            f"{plan['training_split'].replace('_', ' ').title()} Routine"
        ),
        "plan_snapshot": plan,
        "schedule": schedule,
        "created_at": datetime.utcnow().isoformat(),
        "status": "draft",
    }

    validated = WeeklyFitnessRoutine.model_validate(routine_data)

    return {
        **state,
        "weekly_routine": validated.model_dump(),
    }
