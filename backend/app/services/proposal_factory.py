def build_subtask_delete_proposals(
    *,
    analysis: dict
) -> list[dict]:
    proposals = []

    proposals.append({
        "action_type": "delete_subtask",
        "payload": {
            "subtask_id": analysis["deleted_subtask"]
        }
    })

    for r in analysis["rewire_plan"]:
        proposals.append({
            "action_type": "rewire_subtask_dependency",
            "payload": {
                "subtask_id": r["subtask_id"],
                "depends_on_subtask_id": r["new_depends_on"]
            }
        })

    return proposals
