# backend/app/models/goal.py
from sqlalchemy import Column, Integer, String, Text, Date, Float, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Goal(Base):
    __tablename__ = "goals"

    # surrogate PK (simpler and recommended)
    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    goal_name = Column(String(200), nullable=False)
    description = Column(Text)
    percent_completion = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Goal(id={self.goal_id}, user_id={self.user_id}, name='{self.goal_name}')>"
