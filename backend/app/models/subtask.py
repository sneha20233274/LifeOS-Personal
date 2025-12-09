# backend/app/models/subtask.py
from sqlalchemy import (
    Column, Integer, String, Text, Date, Boolean, TIMESTAMP, text,
    PrimaryKeyConstraint, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Subtask(Base):
    __tablename__ = "subtasks"

    subtask_id = Column(Integer, autoincrement=True)
    task_id = Column(Integer)
    goal_id = Column(Integer)
    user_id = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("subtask_id", "task_id", "goal_id", "user_id"),
        ForeignKeyConstraint(
            ["task_id", "goal_id", "user_id"],
            ["tasks.task_id", "tasks.goal_id", "tasks.user_id"],
            ondelete="CASCADE"
        ),
    )

    subtask_name = Column(String(200))
    subtask_description = Column(Text)
    difficulty_rating = Column(Integer, default=1)
    achieved = Column(Boolean, default=False)
    deadline = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))

    task = relationship("Task", back_populates="subtasks")
    user = relationship("User", back_populates="subtasks")
    activities = relationship("Activity", back_populates="subtask", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subtask(subtask_id={self.subtask_id}, task_id={self.task_id}, name='{self.subtask_name}')>"
