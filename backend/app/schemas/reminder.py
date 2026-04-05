from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class ReminderChannel(str, Enum):
    email = "email"
    push = "push"   # future


class ReminderStatus(str, Enum):
    scheduled = "scheduled"
    sent = "sent"
    failed = "failed"


# 🔁 TOGGLE SCHEMA (NEW)
class ReminderToggle(BaseModel):
    hasReminder: bool


# ➕ CREATE CUSTOM REMINDER
class ReminderCreate(BaseModel):
    remind_at: datetime
    channel: ReminderChannel = ReminderChannel.email


# 📤 RESPONSE
class ReminderResponse(BaseModel):
    id: int
    routine_event_id: int
    user_id: int
    remind_at: datetime
    channel: ReminderChannel
    status: ReminderStatus
    sent_at: Optional[datetime]
    
    class Config:
        from_attributes = True
