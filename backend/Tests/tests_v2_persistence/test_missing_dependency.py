from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies


def test_missing_dependency_is_ignored(db):
    proposals_data = [
        {
            "action_type": "create_task",
            "payload": {
                "temp_task_key": "task1",
                "depends_on_task_key": "ghost"
            }
        }
    ]

    saved = save_proposals(
        db=db,
        thread_id="thread-3",
        user_id=1,
        proposals=proposals_data
    )

    apply_dependencies(db, saved)

    assert saved[0].depends_on is None
