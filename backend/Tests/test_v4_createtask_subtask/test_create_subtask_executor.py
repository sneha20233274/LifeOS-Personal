from app.services.Executor.subtask_create import CreateSubtaskExecutor
from my_agent.models.action_proposal import ActionProposal, ProposalStatus
from app.models.subtask import Subtask, SubtaskType
from app.models.task import Task


def test_create_subtask_executor_creates_subtask(db):
    # -----------------------------
    # Existing task in DB
    # -----------------------------
    task = Task(
        user_id=1,
        goal_id=10,
        task_name="Learn Trees",
    )
    db.add(task)
    db.commit()

    # -----------------------------
    # Parent proposal (already executed)
    # -----------------------------
    # Parent task proposal
    create_task_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_task",
        payload={},
        status=ProposalStatus.EXECUTED,
        execution_result={"task_id": task.task_id},
    )
    db.add(create_task_proposal)
    db.commit()  # 👈 REQUIRED

    # Subtask proposal
    create_subtask_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_subtask",
        payload={
            "subtask_name": "Binary Tree Traversals",
            "subtask_type": "count",
            "target_value": 20,
            "order_index": 1,
        },
        status=ProposalStatus.APPROVED,
        depends_on=[create_task_proposal.proposal_id],  # now valid
    )
    db.add(create_subtask_proposal)
    db.commit()


    executor = CreateSubtaskExecutor()

    # -----------------------------
    # Execute
    # -----------------------------
    result = executor.execute(
        db,
        create_subtask_proposal,
        [create_task_proposal, create_subtask_proposal],
    )

    # -----------------------------
    # Assertions
    # -----------------------------
    assert result["status"] == "success"

    subtask = db.query(Subtask).first()
    assert subtask.subtask_name == "Binary Tree Traversals"
    assert subtask.subtask_type == SubtaskType.count
    assert subtask.target_value == 20
    assert subtask.task_id == task.task_id


def test_create_subtask_executor_idempotent(db):
    task = Task(
        user_id=1,
        goal_id=10,
        task_name="Learn Trees",
    )
    db.add(task)
    db.commit()

        # Parent task proposal
    create_task_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_task",
        payload={},
        status=ProposalStatus.EXECUTED,
        execution_result={"task_id": task.task_id},
    )
    db.add(create_task_proposal)
    db.commit()  # 👈 REQUIRED

    # Subtask proposal
    create_subtask_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_subtask",
        payload={
            "subtask_name": "Binary Tree Traversals",
            "subtask_type": "count",
            "target_value": 20,
            "order_index": 1,
        },
        status=ProposalStatus.APPROVED,
        depends_on=[create_task_proposal.proposal_id],  # now valid
    )
    db.add(create_subtask_proposal)
    db.commit()

    executor = CreateSubtaskExecutor()

    result1 = executor.execute(
        db,
        create_subtask_proposal,
        [create_task_proposal, create_subtask_proposal],
    )

    result2 = executor.execute(
        db,
        create_subtask_proposal,
        [create_task_proposal, create_subtask_proposal],
    )

    assert result1["status"] == "success"
    assert result2["data"]["deduplicated"] is True

    subtasks = db.query(Subtask).all()
    assert len(subtasks) == 1


