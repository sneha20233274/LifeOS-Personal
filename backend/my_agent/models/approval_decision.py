from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    TIMESTAMP, text
)
from app.core.database import Base


class ApprovalDecision(Base):
    __tablename__ = "approval_decisions"

    approval_id = Column(Integer, primary_key=True, autoincrement=True)

    proposal_id = Column(
        Integer,
        ForeignKey("action_proposals.proposal_id", ondelete="CASCADE")
    )

    approved_by = Column(Integer, nullable=False)
    decision = Column(String(20), nullable=False)
    comment = Column(String, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )
