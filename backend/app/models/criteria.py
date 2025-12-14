# backend/app/models/criteria.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.orm import relationship
from core.database import Base

class Criteria(Base):
    """
    Semantic descriptors ONLY.
    Examples: coding, backend, meeting, youtube, bugfix
    """
    __tablename__ = "criteria"

    criteria_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    activities = relationship(
        "Activity",
        secondary="activity_criteria",
        back_populates="criteria"
    )
