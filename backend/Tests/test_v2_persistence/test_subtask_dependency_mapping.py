from app.services.proposal_service import save_proposals
from app.services.proposal_dependency_service import apply_dependencies


def test_subtask_dependency_mapping(db):
    proposals_data = [
        {
            "action_type": "create_subtask",
            "payload": {
                "temp_subtask_key": "s1",
                "subtask_name": "Intro"
            }
        },
        {
            "action_type": "create_subtask",
            "payload": {
                "temp_subtask_key": "s2",
                "subtask_name": "Advanced",
                "depends_on_subtask_key": "s1"
            }
        }
    ]

    saved = save_proposals(
        db=db,
        thread_id="thread-4",
        user_id=1,
        proposals=proposals_data
    )

    apply_dependencies(db, saved)

    s1 = next(p for p in saved if p.payload["temp_subtask_key"] == "s1")
    s2 = next(p for p in saved if p.payload["temp_subtask_key"] == "s2")

    assert s2.depends_on == [s1.proposal_id]
