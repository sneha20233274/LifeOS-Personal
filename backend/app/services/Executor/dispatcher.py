from sqlalchemy.orm import Session
from fastapi import HTTPException
from my_agent.models.action_proposal import ActionProposal, ProposalStatus
from app.services.Executor.dependency_guard import can_execute

from app.services.Executor.goal import CreateGoalExecutor
from app.services.Executor.activity import LogActivityExecutor
from app.services.Executor.subtask import UpdateSubtaskExecutor
from app.services.Executor.subtask_delete import DeleteSubtaskExecutor
from app.services.Executor.subtask_rewire import RewireSubtaskDependencyExecutor
from app.services.Executor.create_task import CreateTaskExecutor
from app.services.Executor.subtask_create import CreateSubtaskExecutor
from app.services.Executor.create_fitness_routine import CreateFitnessRoutineExecutor

EXECUTORS = {
    "create_goal": CreateGoalExecutor(),
    "log_activity": LogActivityExecutor(),
    "update_subtask": UpdateSubtaskExecutor(),
    "delete_subtask": DeleteSubtaskExecutor(),
    "rewire_subtask_dependency": RewireSubtaskDependencyExecutor(),
    "create_task": CreateTaskExecutor(),
    "create_subtask": CreateSubtaskExecutor(),
    "create_weekly_fitness_routine" : CreateFitnessRoutineExecutor()

}


def execute_proposals(
    db: Session,
    proposals: list[ActionProposal]
):
    executed = set()
    skipped = set()

    while True:
        progress = False

        for proposal in proposals:
            print(proposal.proposal_id, proposal.action_type, proposal.status)

            if proposal.proposal_id in executed or proposal.proposal_id in skipped:
                continue
            if proposal.status == ProposalStatus.EXECUTED:
                continue
            if proposal.status != ProposalStatus.APPROVED:
                proposal.status = ProposalStatus.SKIPPED
                skipped.add(proposal.proposal_id)
                progress = True
                continue
            

            if not can_execute(proposal, executed):
                continue

            
            print("Executing proposal:", proposal.proposal_id)
            executor = EXECUTORS.get(proposal.action_type)
            if not executor:
                print("No executor for action type:", proposal.action_type)
                proposal.status = ProposalStatus.SKIPPED
                skipped.add(proposal.proposal_id)
                progress = True
                continue


            try:
                result = executor.execute(db, proposal, proposals)
                proposal.execution_result = result["data"]
                proposal.status = ProposalStatus.EXECUTED
                executed.add(proposal.proposal_id)
                db.commit()
                progress = True
                print("Executed proposal:", proposal.proposal_id)

    
            except Exception as e:
                db.rollback()
                proposal.status = ProposalStatus.SKIPPED
                skipped.add(proposal.proposal_id)
                progress = True
                print(f"❌ ERROR executing proposal {proposal.proposal_id}: {e}")
                raise   # <-- IMPORTANT

        if not progress:
            break

    return {
        "executed": list(executed),
        "skipped": list(skipped)
    }
