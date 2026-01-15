def diff_schedules(
    old: list[dict],
    new: list[dict]
) -> list[dict]:
    """
    Identify which subtasks shift in time.
    Compares two versions of a subtask schedule and finds which subtasks changed start date.

It returns only the differences.
    """

    old_map = {s["subtask_id"]: s for s in old}
    diffs = []

    for s in new:
        old_s = old_map.get(s["subtask_id"])
        if not old_s:
            continue

        if s["start_date"] != old_s["start_date"]:
            diffs.append({
                "subtask_id": s["subtask_id"],
                "old_start": old_s["start_date"],
                "new_start": s["start_date"]
            })

    return diffs


def build_reschedule_proposals(schedule_diffs):
    proposals = []

    for d in schedule_diffs:
        proposals.append({
            "action_type": "suggest_reschedule",
            "payload": d
        })

    return proposals
