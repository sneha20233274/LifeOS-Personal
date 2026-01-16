from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, text
)
from app.core.database import Base
from app.services.Executor import activity

# AgentRun represents one execution of your AI agent workflow.
# Each time the user talks to the agent and a LangGraph run starts → one AgentRun row is created.


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

    # | Status           | Meaning                   |
# | ---------------- | ------------------------- |
# | RUNNING          | Agent is executing        |
# | WAITING_APPROVAL | Paused for human approval |
# | COMPLETED        | Finished successfully     |
# | ABORTED          | Cancelled or error        |


    current_node = Column(String(100), nullable=True)
    # Stores the LangGraph node name currently executing.
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        onupdate=text("NOW()")
    )
    # Automatically updates whenever row is modified.

# So you know last activity time.
