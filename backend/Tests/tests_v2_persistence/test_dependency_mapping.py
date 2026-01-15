from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies
from my_agent.models.action_proposal import ActionProposal


def test_task_dependency_mapping(db):
    proposals_data = [
        {
            "action_type": "create_goal",
            "payload": {"goal_name": "Goal"}
        },
        {
            "action_type": "create_task",
            "payload": {
                "temp_task_key": "task1",
                "task_name": "Task 1"
            }
        },
        {
            "action_type": "create_task",
            "payload": {
                "temp_task_key": "task2",
                "task_name": "Task 2",
                "depends_on_task_key": "task1"
            }
        }
    ]

    saved = save_proposals(
        db=db,
        thread_id="thread-2",
        user_id=1,
        proposals=proposals_data
    )

    apply_dependencies(db, saved)
    goal = next(p for p in saved if p.action_type == "create_goal")
    task1 = next(p for p in saved if p.payload.get("temp_task_key") == "task1")
    task2 = next(p for p in saved if p.payload.get("temp_task_key") == "task2")

    assert set(task2.depends_on) == {
        goal.proposal_id,
        task1.proposal_id,
    }

