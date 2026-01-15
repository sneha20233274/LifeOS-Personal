from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    TIMESTAMP,
    text,
    ForeignKey,
    Enum as SAEnum
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ProposalStatus(str, enum.Enum):
    DRAFT = "DRAFT"        # created, not shown to user yet
    PENDING = "PENDING"    # shown to user, waiting for approval
    APPROVED = "APPROVED"  # approved by human
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    SKIPPED = "SKIPPED"


class ActionProposal(Base):
    __tablename__ = "action_proposals"

    proposal_id = Column(Integer, primary_key=True, autoincrement=True)

    # tie proposal to langgraph run
    thread_id = Column(String(100), nullable=False, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    action_type = Column(String(100), nullable=False)

    # JSON payload (editable by human)
    payload = Column(JSON, nullable=False)

    # proposal dependency graph
    depends_on = Column(JSON, nullable=True)  # list[int]

    status = Column(
        SAEnum(ProposalStatus, name="proposal_status_enum"),
        default=ProposalStatus.DRAFT,
        nullable=False,
        index=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )
     # ✅ ONLY NEW FIELD (MINIMAL, POWERFUL)
    execution_result = Column(JSON, nullable=True)
    
    user = relationship("User")

    def __repr__(self):
        return (
            f"<ActionProposal("
            f"id={self.proposal_id}, "
            f"type={self.action_type}, "
            f"status={self.status}"
            f")>"
        )
