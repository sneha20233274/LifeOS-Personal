# backend/app/crud/user_crud.py
from sqlalchemy.orm import Session
from models.user import User
from models.refresh_token import RefreshToken
from core.security import hash_password
from datetime import datetime

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email_id == email).first()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, username: str, email: str, password: str) -> User:
    hashed = hash_password(password)
    user = User(username=username, email_id=email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Refresh token helpers
def save_refresh_token(db: Session, jti: str, token: str, user_id: int, expires_at) -> RefreshToken:
    rt = RefreshToken(jti=jti, token=token, user_id=user_id, expires_at=expires_at)
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt

def revoke_refresh_token(db: Session, jti: str):
    rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if rt:
        rt.revoked = True
        db.add(rt)
        db.commit()
    return rt

def is_refresh_token_revoked(db: Session, jti: str) -> bool:
    rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    return (rt is None) or rt.revoked
