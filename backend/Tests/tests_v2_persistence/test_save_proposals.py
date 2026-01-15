from app.services.proposal_service import save_proposals
from my_agent.models.action_proposal import ProposalStatus, ActionProposal


def test_save_proposals(db):
    proposals_data = [
        {
            "action_type": "create_goal",
            "payload": {"goal_name": "Test Goal"}
        },
        {
            "action_type": "create_task",
            "payload": {
                "temp_task_key": "task1",
                "task_name": "Task A"
            }
        }
    ]

    saved = save_proposals(
        db=db,
        thread_id="thread-1",
        user_id=1,
        proposals=proposals_data
    )

    assert len(saved) == 2

    db_proposals = db.query(ActionProposal).all()
    assert len(db_proposals) == 2

    assert db_proposals[0].status == ProposalStatus.PENDING
    assert db_proposals[1].payload["temp_task_key"] == "task1"
