from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# ✅ Direct connection (NO psycopg_pool)
conn = psycopg.connect(
    DATABASE_URL,
    prepare_threshold=0   # ✅ required for Supabase pooler
)

# ✅ Pass direct connection to LangGraph
checkpointer = PostgresSaver(conn=conn)