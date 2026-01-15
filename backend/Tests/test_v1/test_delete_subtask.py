from app.services.Executor.dispatcher import execute_proposals
from app.models.subtask import Subtask, SubtaskType
from my_agent.models.action_proposal import ActionProposal, ProposalStatus


def test_delete_subtask(db):
    # -----------------------------
    # Setup: existing subtask
    # -----------------------------
    subtask = Subtask(
        user_id=1,
        task_id=1,
        subtask_name="Test Subtask",
        subtask_type=SubtaskType.checkbox,
        order_index=1,
    )
    db.add(subtask)
    db.commit()

    subtask_id = subtask.subtask_id

    # -----------------------------
    # Proposal: delete subtask
    # -----------------------------
    proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="delete_subtask",
        payload={"subtask_id": subtask_id},
        status=ProposalStatus.APPROVED,
    )
    db.add(proposal)
    db.commit()

    # -----------------------------
    # Execute
    # -----------------------------
    result = execute_proposals(db=db, proposals=[proposal])

    # -----------------------------
    # Assertions
    # -----------------------------
    assert proposal.status == ProposalStatus.EXECUTED
    assert subtask_id in result["executed"]

    # subtask must be deleted
    assert db.get(Subtask, subtask_id) is None
