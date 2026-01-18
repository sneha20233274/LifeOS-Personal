

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class RoutineEvent(Base):
    __tablename__ = "routine_events"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title = Column(String(255), nullable=False)
    description = Column(Text, default="")

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_all_day = Column(Boolean, default=False)

    category = Column(String(100), default="General")
    priority = Column(String(20), default="Medium")
    status = Column(String(20), default="Scheduled")

    location_or_link = Column(String(255), nullable=True)

    source = Column(String(20), default="manual")
    calendar_event_id = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Optional ORM relationship (not required yet)
    user = relationship("User", back_populates="routine_events")
