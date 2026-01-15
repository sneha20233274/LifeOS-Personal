from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    TIMESTAMP, text
)
from app.core.database import Base

# It stores human decisions on AI-generated proposals.
# Every time a human clicks Approve / Reject, one row is inserted here.

# So:

# ApprovalDecision = Audit log of human judgment.

class ApprovalDecision(Base):
    __tablename__ = "approval_decisions"

    approval_id = Column(Integer, primary_key=True, autoincrement=True)

    proposal_id = Column(
        Integer,
        ForeignKey("action_proposals.proposal_id", ondelete="CASCADE")
    )
#     ondelete="CASCADE"

# If proposal is deleted → decision auto deletes.

    approved_by = Column(Integer, nullable=False)
    # Which human user approved/rejected.
    decision = Column(String(20), nullable=False)
    # APPROVED | REJECTED
    comment = Column(String, nullable=True)
    # Optional explanation from human.

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )
