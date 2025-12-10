# backend/app/models/activity.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    subtask_id = Column(Integer, ForeignKey("subtasks.subtask_id", ondelete="SET NULL"), nullable=True)

    activity_name = Column(String(200))
    activity_description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="activities")
    subtask = relationship("Subtask", back_populates="activities")

    def __repr__(self):
        return f"<Activity(id={self.activity_id}, user_id={self.user_id})>"
