from app.services.Executor.dispatcher import execute_proposals
from my_agent.models.action_proposal import ActionProposal, ProposalStatus


def test_idempotent_execution(db):
    # -----------------------------
    # Proposal: delete non-existing subtask
    # -----------------------------
    proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="delete_subtask",
        payload={"subtask_id": 999},  # does not exist
        status=ProposalStatus.APPROVED,
    )

    db.add(proposal)
    db.commit()

    proposal_id = proposal.proposal_id

    # -----------------------------
    # First execution
    # -----------------------------
    result1 = execute_proposals(db=db, proposals=[proposal])

    assert proposal.status == ProposalStatus.EXECUTED
    assert proposal_id in result1["executed"]

    # -----------------------------
    # Second execution (resume)
    # -----------------------------
    result2 = execute_proposals(db=db, proposals=[proposal])

    # NOTHING should execute again
    assert result2["executed"] == []

    # proposal remains executed
    assert proposal.status == ProposalStatus.EXECUTED
