from app.services.Executor.create_task import CreateTaskExecutor
from my_agent.models.action_proposal import ActionProposal, ProposalStatus
from app.models.task import Task


def test_create_task_executor_creates_task(db):
    executor = CreateTaskExecutor()

    # -----------------------------
    # Parent goal proposal
    # -----------------------------
    create_goal_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_goal",
        payload={},
        status=ProposalStatus.EXECUTED,
        execution_result={"goal_id": 10},
    )
    db.add(create_goal_proposal)
    db.commit()  # ✅ IMPORTANT

    # -----------------------------
    # Task proposal (depends on goal)
    # -----------------------------
    create_task_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_task",
        payload={
            "task_name": "Learn Trees",
            "description": "Binary trees and BSTs",
            "difficulty": 2,
        },
        status=ProposalStatus.APPROVED,
        depends_on=[create_goal_proposal.proposal_id],  # now valid
    )
    db.add(create_task_proposal)
    db.commit()

    # -----------------------------
    # Execute
    # -----------------------------
    result = executor.execute(
        db,
        create_task_proposal,
        [create_goal_proposal, create_task_proposal],
    )

    # -----------------------------
    # Assertions
    # -----------------------------
    assert result["status"] == "success"

    task = db.query(Task).first()
    assert task is not None
    assert task.task_name == "Learn Trees"
    assert task.goal_id == 10
    assert task.difficulty == 2


def test_create_task_executor_idempotent(db):
    executor = CreateTaskExecutor()

    create_goal_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_goal",
        payload={},
        status=ProposalStatus.EXECUTED,
        execution_result={"goal_id": 10},
    )
    db.add(create_goal_proposal)
    db.commit()

    create_task_proposal = ActionProposal(
        thread_id="t1",
        user_id=1,
        action_type="create_task",
        payload={"task_name": "Learn Trees"},
        status=ProposalStatus.APPROVED,
        depends_on=[create_goal_proposal.proposal_id],
    )
    db.add(create_task_proposal)
    db.commit()

    result1 = executor.execute(
        db,
        create_task_proposal,
        [create_goal_proposal, create_task_proposal],
    )

    result2 = executor.execute(
        db,
        create_task_proposal,
        [create_goal_proposal, create_task_proposal],
    )

    assert result1["status"] == "success"
    assert result2["data"]["deduplicated"] is True

    tasks = db.query(Task).all()
    assert len(tasks) == 1
