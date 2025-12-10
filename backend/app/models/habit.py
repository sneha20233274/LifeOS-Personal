# backend/app/models/habit.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Habit(Base):
    __tablename__ = "habits"
    habit_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    target_minutes = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="habits")

    def __repr__(self):
        return f"<Habit(id={self.habit_id}, name='{self.name}', user_id={self.user_id})>"
