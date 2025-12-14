# backend/app/models/goal.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    TIMESTAMP,
    text,
    ForeignKey,
    Date,
    JSON,
)
from sqlalchemy.orm import relationship
from core.database import Base


class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    goal_name = Column(String(200), nullable=False)
    description = Column(Text)

    # 🎯 Optional target date
    target_date = Column(Date, nullable=True)

    # 💡 USER-OWNED metadata
    importance_level = Column(Integer, default=1)   # 1–5 scale (soft meaning)
    motivations = Column(JSON, nullable=True)       # list[str] or structured JSON

    # 🔒 SYSTEM MANAGED
    percent_completion = Column(Float, default=0.0)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Goal(id={self.goal_id}, completion={self.percent_completion})>"
