# backend/app/models/summary.py

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Date, text
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Summary(Base):
    __tablename__ = "summaries"

    summary_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    # daily | weekly | goal
    summary_type = Column(String(20), nullable=False)

    # for daily / weekly
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)

    # for goal summary
    goal_id = Column(
        Integer,
        ForeignKey("goals.goal_id", ondelete="CASCADE"),
        nullable=True
    )

    # 🔢 STRUCTURED ANALYTICS (FOR UI + GRAPHS)
    metrics = Column(JSON, nullable=False)

    # 🧠 SEMANTIC TEXT (FOR RAG + CHATBOT)
    narrative = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    user = relationship("User")
    goal = relationship("Goal")
