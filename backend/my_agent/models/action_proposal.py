from sqlalchemy import (
    Column, Integer, String, ForeignKey, JSON,
    TIMESTAMP, text
)
from app.core.database import Base


class ActionProposal(Base):
    __tablename__ = "action_proposals"

    proposal_id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("agent_runs.run_id", ondelete="CASCADE"))

    action_type = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=False)

    status = Column(
        String(20),
        default="DRAFT"
        # DRAFT | APPROVED | REJECTED | EXECUTED
    )

    reason = Column(String, nullable=True)

    version = Column(Integer, default=1)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )
