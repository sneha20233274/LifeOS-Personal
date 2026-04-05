# backend/app/core/config.py
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Snehaash%401410@db.xofuzpjnjbbhxacxekip.supabase.co:5432/postgres")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-to-a-secure-random-string")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "5"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
