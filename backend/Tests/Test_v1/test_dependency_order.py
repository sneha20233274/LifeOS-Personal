from app.services.Executor.dispatcher import execute_proposals
from app.models.subtask import Subtask, SubtaskType
from my_agent.models.action_proposal import ActionProposal, ProposalStatus


def test_partial_approval(db):
    subtask = Subtask(
        user_id=1,
        task_id=1,
        subtask_name="X",
        subtask_type=SubtaskType.checkbox,
        order_index=1
    )
    db.add(subtask)
    db.commit()

    approved = ActionProposal(
        proposal_id=1,
        thread_id="t1",
        user_id=1,
        action_type="delete_subtask",
        payload={"subtask_id": subtask.subtask_id},
        status=ProposalStatus.APPROVED
    )

    rejected = ActionProposal(
        proposal_id=2,
        thread_id="t1",
        user_id=1,
        action_type="rewire_subtask_dependency",
        payload={"subtask_id": 999},
        status=ProposalStatus.REJECTED
    )

    db.add_all([approved, rejected])
    db.commit()

    result = execute_proposals(db=db, proposals=[approved, rejected])

    assert approved.proposal_id in result["executed"]
    assert rejected.proposal_id in result["skipped"]
