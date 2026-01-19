from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base


class GoogleToken(Base):
    __tablename__ = "google_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)

    token_uri = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)

    scopes = Column(String, nullable=False)

    expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
