# backend/app/models/activity.py
#from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text, ForeignKey
#from sqlalchemy.orm import relationship
#from core.database import Base

#class Activity(Base):
#    __tablename__ = "activities"

#    activity_id = Column(Integer, primary_key=True, autoincrement=True)
#    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
#    subtask_id = Column(Integer, ForeignKey("subtasks.subtask_id", ondelete="SET NULL"), nullable=True)

#    activity_name = Column(String(200))
#    activity_description = Column(Text)
#    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

#    user = relationship("User", back_populates="activities")
#    subtask = relationship("Subtask", back_populates="activities")

#    def __repr__(self):
#        return f"<Activity(id={self.activity_id}, user_id={self.user_id})>"


# backend/app/models/activity.py
from sqlalchemy import (
    Column, Integer, String, Text, TIMESTAMP, text,
    ForeignKey, Enum as SAEnum, Float, JSON, Table
)
from sqlalchemy.orm import relationship
from core.database import Base
from models.enums import SummaryCategoryEnum


activity_criteria = Table(
    "activity_criteria",
    Base.metadata,
    Column("activity_id", Integer, ForeignKey("activities.activity_id", ondelete="CASCADE"), primary_key=True),
    Column("criteria_id", Integer, ForeignKey("criteria.criteria_id", ondelete="CASCADE"), primary_key=True),
)


class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    # ✅ OPTIONAL relationship (this is correct)
    subtask_id = Column(
        Integer,
        ForeignKey("subtasks.subtask_id", ondelete="SET NULL"),
        nullable=True
    )

    activity_name = Column(String(200))
    activity_description = Column(Text)

    # ---- TIME (authoritative) ----
    start_ts = Column(TIMESTAMP(timezone=True))
    end_ts = Column(TIMESTAMP(timezone=True))
    duration_minutes = Column(Integer, nullable=False)

    # ---- SINGLE counting bucket ----
    summary_category = Column(
        SAEnum(SummaryCategoryEnum, name="summary_category_enum"),
        nullable=False,
        index=True
    )

    # ---- SEMANTIC ONLY ----
    criteria = relationship(
        "Criteria",
        secondary=activity_criteria,
        back_populates="activities"
    )

    # ---- METADATA ----
    app_name = Column(String(100))
    domain = Column(String(255))
    device = Column(String(50))
    source = Column(String(50))
    focus_score = Column(Float)

    # ---- FUTURE AI (v3 safe) ----
    ml_output = Column(JSON)
    llm_reasoning = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="activities")
    subtask = relationship("Subtask", back_populates="activities")



