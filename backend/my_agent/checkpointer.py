from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# ✅ FIX: remove "+psycopg"
RAW_DB_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

# ✅ direct connection
conn = psycopg.connect(
    RAW_DB_URL,
    prepare_threshold=0
)

checkpointer = PostgresSaver(conn=conn)