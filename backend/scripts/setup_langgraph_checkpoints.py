# scripts/setup_langgraph_checkpoints.py

import os
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# 🔑 IMPORTANT: autocommit=True
conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
)

checkpointer = PostgresSaver(conn=conn)

# ✅ This will now succeed
checkpointer.setup()

print("✅ LangGraph checkpoint tables created successfully.")
