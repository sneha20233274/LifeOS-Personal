# backend/app/models/subtask.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    TIMESTAMP,
    text,
    ForeignKey,
    Enum as SAEnum,
    Float
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


# -----------------------------
# Subtask completion strategies
# -----------------------------
class SubtaskType(enum.Enum):
    checkbox = "checkbox"     # manual / binary
    count = "count"           # e.g. solve 50 problems
    duration = "duration"     # e.g. study 600 minutes
    score = "score"           # e.g. score >= 8


class Subtask(Base):
    __tablename__ = "subtasks"

    # -------- primary key --------
    subtask_id = Column(Integer, primary_key=True, autoincrement=True)

    # -------- ownership --------
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.task_id", ondelete="CASCADE"),
        nullable=False
    )

    # optional redundancy (safe, not required)
    goal_id = Column(
        Integer,
        ForeignKey("goals.goal_id", ondelete="CASCADE"),
        nullable=True
    )

    # -------- core fields --------
    subtask_name = Column(String(200), nullable=False)

    subtask_type = Column(
        SAEnum(SubtaskType, name="subtask_type_enum"),
        nullable=False
    )

    # -------- progress state --------
    # ❗ derived state — never set at creation
    achieved = Column(Boolean, default=False, nullable=False)

    # used only for non-checkbox subtasks
    target_value = Column(Float, nullable=True)
    current_value = Column(Float, default=0.0, nullable=False)

    # contribution to task completion
    weight = Column(Integer, default=1, nullable=False)

    # -------- dependency graph --------
    depends_on_subtask_id = Column(
        Integer,
        ForeignKey("subtasks.subtask_id", ondelete="SET NULL"),
        nullable=True
    )

    # -------- scheduling --------
    deadline = Column(Date)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    # -------- relationships --------
    task = relationship("Task", back_populates="subtasks")
    user = relationship("User", back_populates="subtasks")

    activities = relationship(
        "Activity",
        back_populates="subtask",
        cascade="all, delete-orphan"
    )

    # self-referential dependency
    depends_on = relationship(
        "Subtask",
        remote_side=[subtask_id],
        uselist=False
    )

    def __repr__(self) -> str:
        return (
            f"<Subtask("
            f"id={self.subtask_id}, "
            f"type={self.subtask_type}, "
            f"achieved={self.achieved}"
            f")>"
        )
