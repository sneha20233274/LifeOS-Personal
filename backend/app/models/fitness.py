from sqlalchemy import Column, Integer, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base


class UserFitnessRoutinesDB(Base):
    __tablename__ = "user_fitness_routines"

    user_id = Column(Integer, primary_key=True)

    routines = Column(JSONB, nullable=False)

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
