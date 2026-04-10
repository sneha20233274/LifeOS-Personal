from langgraph.checkpoint.postgres import PostgresSaver
import psycopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# convert URL for psycopg
RAW_DB_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

# ✅ create ONE connection (not function)
conn = psycopg.connect(
    RAW_DB_URL,
    prepare_threshold=0,
    connect_timeout=10,
    autocommit=True
)

# ✅ pass connection (correct)
checkpointer = PostgresSaver(conn=conn)