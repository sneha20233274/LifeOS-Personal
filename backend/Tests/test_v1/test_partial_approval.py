from app.services.Executor.dispatcher import execute_proposals
from app.models.subtask import Subtask, SubtaskType
from my_agent.models.action_proposal import ActionProposal, ProposalStatus


def test_rewire_dependency(db):
    # -----------------------------
    # Setup subtasks
    # -----------------------------
    a = Subtask(
        user_id=1,
        task_id=1,
        subtask_name="A",
        subtask_type=SubtaskType.checkbox,
        order_index=1,
    )
    b = Subtask(
        user_id=1,
        task_id=1,
        subtask_name="B",
        subtask_type=SubtaskType.checkbox,
        order_index=2,
    )
    db.add_all([a, b])
    db.commit()

    # -----------------------------
    # Proposal: rewire B → A
    # -----------------------------
    proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="rewire_subtask_dependency",
        payload={
            "subtask_id": b.subtask_id,
            "depends_on_subtask_id": a.subtask_id,
        },
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
    assert proposal.proposal_id in result["executed"]

    db.refresh(b)
    assert b.depends_on_subtask_id == a.subtask_id
