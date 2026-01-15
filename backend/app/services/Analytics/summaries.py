# backend/app/services/analytics/summaries.py

"""
This module converts structured analytics (metrics)
into human-readable semantic summaries.

RULES:
- Input = metrics dict (already computed)
- Output = clean natural language
- NO database calls
- NO math / analytics
"""

# --------------------------------------------------
# DAILY SUMMARY
# --------------------------------------------------

def daily_summary(user, stats: dict) -> str:
    """
    stats expected keys:
    - total_minutes
    - productive_minutes
    - productivity_ratio
    - time_by_category
    - top_criteria
    - task_completion
    - peak_category
    - top_non_productive_category
    """

    return f"""
Daily Summary for {user.name}

Time Overview
• Total time logged: {stats['total_minutes']} minutes
• Productive time: {stats['productive_minutes']} minutes
• Productivity ratio: {stats['productivity_ratio']:.0%}

Activity Breakdown
• Most productive category: {stats.get('peak_category') or 'N/A'}
• Biggest time sink: {stats.get('top_non_productive_category') or 'N/A'}

Top Focus Areas
{_format_key_values(stats.get('top_criteria'))}

Execution
• Task completion rate: {stats['task_completion']:.0%}

Reflection
You were most effective when working on
{stats.get('peak_category') or 'your key activities'}.
""".strip()


# --------------------------------------------------
# WEEKLY SUMMARY
# --------------------------------------------------

def weekly_summary(user, stats: dict) -> str:
    """
    stats expected keys:
    - weekly_productive_minutes
    - delta_percent
    - top_goals
    - top_habit
    - focus_pattern
    """

    trend = (
        "improved" if stats["delta_percent"] > 0
        else "declined" if stats["delta_percent"] < 0
        else "remained stable"
    )

    return f"""
Weekly Summary for {user.name}

Productivity
• Total productive time: {stats['weekly_productive_minutes']} minutes
• Change vs last week: {stats['delta_percent']:+.1f}% ({trend})

Goals Progressed
{_format_list(stats.get('top_goals'))}

Habits
• Most consistent habit: {stats.get('top_habit') or 'Not enough data'}

Focus Insight
{stats.get('focus_pattern') or 'No clear focus pattern detected this week.'}
""".strip()


# --------------------------------------------------
# GOAL NARRATIVE (RAG GOLD)
# --------------------------------------------------

def goal_narrative(goal, progress: float) -> str:
    """
    Generates semantic memory for a goal.
    """

    status = (
        "On track" if progress >= 70
        else "Making progress" if progress >= 40
        else "Needs attention"
    )

    motivations = (
        ", ".join(goal.motivations)
        if isinstance(goal.motivations, list)
        else goal.motivations
        if goal.motivations
        else "Not specified"
    )

    return f"""
Goal Progress Summary

Goal: {goal.goal_name}
Current completion: {progress:.1f}%
Status: {status}

Importance level: {goal.importance_level}

Motivations:
{motivations}

Guidance:
Focus on the subtasks with the lowest completion
to increase momentum on this goal.
""".strip()


# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------

def _format_key_values(data: dict | None) -> str:
    """
    Formats dict like:
    {"coding": 180, "meeting": 60}
    """
    if not data:
        return "• No significant data available"

    return "\n".join(
        f"• {key}: {value} minutes"
        for key, value in data.items()
    )


def _format_list(items: list | None) -> str:
    if not items:
        return "• None"

    return "\n".join(f"• {item}" for item in items)
