# backend/app/schemas/token.py
from pydantic import BaseModel
from typing import Optional

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenRefresh(BaseModel):
    refresh_token: str
