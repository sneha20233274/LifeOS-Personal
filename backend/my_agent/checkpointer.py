from langgraph.checkpoint.postgres import PostgresSaver
import psycopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

RAW_DB_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

def get_checkpointer():
    conn = psycopg.connect(
        RAW_DB_URL,
        connect_timeout=10,
        autocommit=True
    )
    checkpointer = PostgresSaver(conn=conn)
    checkpointer.setup()

    return checkpointer