from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, text
)
from app.core.database import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    run_id = Column(String, primary_key=True)  # UUID / thread_id
    user_id = Column(Integer, nullable=False)

    status = Column(
        String(32),
        nullable=False,
        default="RUNNING"
        # RUNNING | WAITING_APPROVAL | COMPLETED | ABORTED
    )

    current_node = Column(String(100), nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        onupdate=text("NOW()")
    )
