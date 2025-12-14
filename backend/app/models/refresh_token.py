# backend/app/models/refresh_token.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(128), unique=True, nullable=False)   # token id (from JWT jti)
    token = Column(String, nullable=False)                    # the JWT string (optional, but handy for debugging)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    revoked = Column(Boolean, default=False)
    expires_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshToken(jti={self.jti}, user_id={self.user_id}, revoked={self.revoked})>"
