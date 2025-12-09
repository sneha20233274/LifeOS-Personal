# backend/app/models/goal.py
from sqlalchemy import (
    Column, Integer, String, Text, Date, Float, TIMESTAMP, text,
    PrimaryKeyConstraint, ForeignKey
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Goal(Base):
    __tablename__ = "goals"

    # composite PK (goal_id, user_id)
    goal_id = Column(Integer, autoincrement=True)
    user_id = Column(Integer)  # FK set below
    __table_args__ = (
        PrimaryKeyConstraint("goal_id", "user_id"),
    )

    # foreign key to users.user_id
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    goal_name = Column(String(200), nullable=False)
    description = Column(Text)
    deadline = Column(Date)
    importance_level = Column(Integer, default=1)   # 1..5
    percent_completion = Column(Float, default=0.0)
    motivations = Column(Text)  # JSON/text list; could be ARRAY/Text[] if postgres
    metadata = Column(Text)     # free-form JSON string or use JSON type
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))

    user = relationship("User", back_populates="goals")
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Goal(goal_id={self.goal_id}, user_id={self.user_id}, name='{self.goal_name}')>"
