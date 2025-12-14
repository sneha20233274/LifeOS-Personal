# backend/app/models/notification.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200))
    body = Column(String(1000))
    scheduled_time = Column(TIMESTAMP(timezone=True))
    sent = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.notification_id}, user_id={self.user_id}, title='{self.title}')>"
