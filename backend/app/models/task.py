# backend/app/models/task.py
from sqlalchemy import (
    Column, Integer, String, Text, Date, Float, TIMESTAMP, text,
    ForeignKey, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    # primary key columns: task_id (autoincrement), goal_id, user_id
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    goal_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    # Foreign key constraint referencing Goal's composite (goal_id, user_id)
    __table_args__ = (
        ForeignKeyConstraint(
            ["goal_id", "user_id"],
            ["goals.goal_id", "goals.user_id"],
            ondelete="CASCADE"
        ),
    )

    task_name = Column(String(200), nullable=False)
    task_description = Column(Text)
    task_deadline = Column(Date)
    difficulty_level = Column(Integer, default=1)
    percent_completion = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))

    # relationships
    goal = relationship(
        "Goal",
        back_populates="tasks",
        primaryjoin="and_(Task.goal_id==Goal.goal_id, Task.user_id==Goal.user_id)"
    )
    user = relationship("User", back_populates="tasks", foreign_keys=[user_id])
    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, goal_id={self.goal_id}, user_id={self.user_id}, name='{self.task_name}')>"
