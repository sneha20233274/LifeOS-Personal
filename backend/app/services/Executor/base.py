from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.orm import Session
from my_agent.models.action_proposal import ActionProposal


class ExecutorResult(dict):
    """
    Simple structured result:
    {
        "status": "success" | "error",
        "data": {...}
    }
    """
    pass


class BaseExecutor(ABC):
    action_type: str

    @abstractmethod
    def execute(
        self,
        db: Session,
        proposal: ActionProposal
    ) -> ExecutorResult:
        pass
