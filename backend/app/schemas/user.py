# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email_id: EmailStr
    password: str
    timezone: Optional[str] = "UTC"
    
class UserLogin(BaseModel):
    email_id: str
    password: str

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
class UserOut(BaseModel):
    user_id: int
    username: str
    email_id: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
