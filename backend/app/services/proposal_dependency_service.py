from sqlalchemy.orm import Session
from my_agent.models.action_proposal import ActionProposal


def apply_dependencies(
    db: Session,
    proposals: list[ActionProposal]
):
    """
    Populate ActionProposal.depends_on using temp keys in payload.
    """

    # temp_key -> proposal_id
    temp_map = {}

    for p in proposals:
        payload = p.payload or {}

        if "temp_task_key" in payload:
            temp_map[payload["temp_task_key"]] = p.proposal_id

        if "temp_subtask_key" in payload:
            temp_map[payload["temp_subtask_key"]] = p.proposal_id

    for p in proposals:
        payload = p.payload or {}
        deps = []

        # task → task
        parent_task = payload.get("depends_on_task_key")
        if parent_task and parent_task in temp_map:
            deps.append(temp_map[parent_task])

        # subtask → subtask
        parent_subtask = payload.get("depends_on_subtask_key")
        if parent_subtask and parent_subtask in temp_map:
            deps.append(temp_map[parent_subtask])

        # task → goal (structural rule)
        if p.action_type == "create_task":
            goal = next(
                (x for x in proposals if x.action_type == "create_goal"),
                None
            )
            if goal:
                deps.append(goal.proposal_id)

        if deps:
            p.depends_on = list(set(deps))

    db.commit()
