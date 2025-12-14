# backend/app/models/subtask.py
from sqlalchemy import (
    Column, Integer, String, Text, Date, Boolean, TIMESTAMP, text,
    ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base

class Subtask(Base):
    __tablename__ = "subtasks"

    # single surrogate PK makes ORM joins trivial
    subtask_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    # goal_id is optional because task->goal relationship exists; include if you want redundancy
    goal_id = Column(Integer, ForeignKey("goals.goal_id", ondelete="CASCADE"), nullable=True)

    subtask_name = Column(String(200))
    achieved = Column(Boolean, default=False)
    deadline = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    # relationships
    task = relationship("Task", back_populates="subtasks")
    user = relationship("User", back_populates="subtasks")
    activities = relationship("Activity", back_populates="subtask", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subtask(id={self.subtask_id}, task_id={self.task_id}, user_id={self.user_id})>"
