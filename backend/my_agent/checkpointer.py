from langgraph.checkpoint.postgres import PostgresSaver
import psycopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# convert URL for psycopg
RAW_DB_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

# ✅ create NEW connection every time
def get_conn():
    return psycopg.connect(
        RAW_DB_URL,
        prepare_threshold=0,
        connect_timeout=10
    )

# ✅ pass function, not connection
checkpointer = PostgresSaver(conn=get_conn)