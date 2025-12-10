# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    email_id = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    timezone = Column(String(64), default="UTC")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    # relationships
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    subtasks = relationship("Subtask", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
    time_logs = relationship("TimeLog", back_populates="user", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email_id}')>"
