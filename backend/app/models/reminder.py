from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)

    routine_event_id = Column(
        Integer,
        ForeignKey("routine_events.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    remind_at = Column(DateTime, nullable=False)

    channel = Column(String(20), default="email")
    status = Column(String(20), default="scheduled")

    sent_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ORM relationships
    user = relationship(
        "User",
        back_populates="reminders"
    )

    routine_event = relationship(
        "RoutineEvent",
        back_populates="reminders"
    )
