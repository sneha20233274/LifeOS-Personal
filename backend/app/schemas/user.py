# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email_id: EmailStr
    password: str
    timezone: Optional[str] = "UTC"

class UserUpdate(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    timezone: Optional[str]

class UserOut(BaseModel):
    user_id: int
    username: str
    email_id: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
