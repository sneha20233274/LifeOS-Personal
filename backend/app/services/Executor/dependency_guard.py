from my_agent.models.action_proposal import ProposalStatus


def can_execute(proposal, executed_ids: set[int]) -> bool:
    """
    Proposal can execute only if:
    - approved
    - all dependencies already executed
    """
    if proposal.status != ProposalStatus.APPROVED:
        return False

    if not proposal.depends_on:
        return True
   
    return all(dep_id in executed_ids for dep_id in proposal.depends_on)
