# backend/app/models/task.py

from sqlalchemy import (
    Column, Integer, String, Text, Float,
    Boolean, ForeignKey, TIMESTAMP, text
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    goal_id = Column(
        Integer,
        ForeignKey("goals.goal_id", ondelete="CASCADE"),
        nullable=False
    )

    task_name = Column(String(200), nullable=False)
    description = Column(Text)

    # weighted contribution to goal
    difficulty = Column(Integer, default=1, nullable=False)

    # derived state
    percent_completion = Column(Float, default=0.0, nullable=False)
    achieved = Column(Boolean, default=False)

    # -------- dependency (task → task) --------
    depends_on_task_id = Column(
        Integer,
        ForeignKey("tasks.task_id", ondelete="SET NULL"),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    # relationships
    goal = relationship("Goal", back_populates="tasks")
    user = relationship("User", back_populates="tasks")

    subtasks = relationship(
        "Subtask",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    depends_on = relationship(
        "Task",
        remote_side=[task_id],
        uselist=False
    )

    def __repr__(self):
        return f"<Task(id={self.task_id}, completion={self.percent_completion})>"
