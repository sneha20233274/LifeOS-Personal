# backend/app/models/task.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Float,
    TIMESTAMP,
    text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    # -------------------------
    # PRIMARY KEY
    # -------------------------
    task_id = Column(Integer, primary_key=True, autoincrement=True)

    # -------------------------
    # OPTIONAL GOAL LINK
    # -------------------------
    goal_id = Column(
        Integer,
        ForeignKey("goals.goal_id", ondelete="SET NULL"),
        nullable=True,            # ✅ NOW OPTIONAL
        index=True,
    )

    # -------------------------
    # OWNER (ALWAYS REQUIRED)
    # -------------------------
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # -------------------------
    # TASK DATA
    # -------------------------
    task_name = Column(String(200), nullable=False)
    task_description = Column(Text)

    task_deadline = Column(Date)

    difficulty_level = Column(Integer, default=1)
    percent_completion = Column(Float, default=0.0)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        onupdate=text("NOW()"),
    )

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    goal = relationship(
        "Goal",
        back_populates="tasks",
    )

    user = relationship(
        "User",
        back_populates="tasks",
    )

    subtasks = relationship(
        "Subtask",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Task(task_id={self.task_id}, "
            f"goal_id={self.goal_id}, "
            f"user_id={self.user_id}, "
            f"name='{self.task_name}')>"
        )
