# app/models/weekly_fitness_routine.py
from sqlalchemy import Column, String, DateTime, Enum, JSON
from app.core.database import Base
from datetime import datetime
import enum


class RoutineStatus(enum.Enum):
    draft = "draft"
    approved = "approved"


class WeeklyFitnessRoutineDB(Base):
    __tablename__ = "weekly_fitness_routines"

    routine_id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)

    routine_name = Column(String, nullable=False)

    # 🔥 EXACT LLM OUTPUT (NO TRANSFORMATION)
    plan_snapshot = Column(JSON, nullable=False)
    schedule = Column(JSON, nullable=False)

    status = Column(Enum(RoutineStatus), default=RoutineStatus.draft)

    created_at = Column(DateTime, default=datetime.utcnow)
