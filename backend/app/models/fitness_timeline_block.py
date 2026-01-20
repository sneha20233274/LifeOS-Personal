# app/models/fitness_timeline_block.py
from sqlalchemy import Column, String, JSON, ForeignKey
from app.core.database import Base


class FitnessTimelineBlockDB(Base):
    __tablename__ = "fitness_timeline_blocks"

    id = Column(String, primary_key=True)
    routine_id = Column(
        String,
        ForeignKey("weekly_fitness_routines.routine_id", ondelete="CASCADE"),
        index=True
    )

    day = Column(String)               # monday, tuesday...
    time_range = Column(String)        # "07:00-07:10"
    block_type = Column(String)        # warmup, exercise
    category = Column(String)          # strength, cardio, mobility
    details = Column(JSON, nullable=True)
