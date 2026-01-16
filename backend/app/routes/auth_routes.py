# backend/app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError
from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserOut,UserLogin
from app.schemas.token import TokenOut, TokenRefresh
from app.crud.user_crud import create_user, get_user_by_email, save_refresh_token, revoke_refresh_token, is_refresh_token_revoked, get_user
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.models.refresh_token import RefreshToken
from app.models.user import User

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email_id)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload.username, payload.email_id, payload.password)
    return user

@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    # Using same schema as UserCreate for simple login (email + password)
    user = get_user_by_email(db, payload.email_id)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token(subject=str(user.user_id))
    refresh = create_refresh_token(subject=str(user.user_id))
    # Save refresh token jti and expiry
    decoded = decode_token(refresh)
    jti = decoded.get("jti")
    exp_ts = datetime.utcfromtimestamp(decoded.get("exp"))
    save_refresh_token(db, jti=jti, token=refresh, user_id=user.user_id, expires_at=exp_ts)
    return TokenOut(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=TokenOut)
def refresh_token(payload: TokenRefresh, db: Session = Depends(get_db)):
    print("==== REFRESH TOKEN DEBUG START ====")
    print("Incoming refresh token:", payload.refresh_token)

    try:
        decoded = decode_token(payload.refresh_token)
        print("Decoded token payload:", decoded)

        token_type = decoded.get("type")
        print("Token type:", token_type)

        if token_type != "refresh":
            print("❌ Token type mismatch")
            raise HTTPException(status_code=401, detail="Invalid token type")

        jti = decoded.get("jti")
        print("Extracted JTI from token:", jti)

        is_revoked = is_refresh_token_revoked(db, jti)
        print("Is token revoked according to DB?", is_revoked)

        if is_revoked:
            print("❌ Token is considered revoked")
            raise HTTPException(status_code=401, detail="Token revoked")

        user_id = decoded.get("sub")
        print("User ID from token:", user_id)

    except JWTError as e:
        print("❌ JWT Error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access = create_access_token(subject=str(user_id))
    print("✅ New access token generated")
    print("==== REFRESH TOKEN DEBUG END ====")

    return TokenOut(access_token=access, refresh_token=payload.refresh_token)


@router.post("/logout")
def logout(payload: TokenRefresh, db: Session = Depends(get_db)):
    # revoke the provided refresh token
    try:
        decoded = decode_token(payload.refresh_token)
        jti = decoded.get("jti")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    rt = revoke_refresh_token(db, jti)
    if not rt:
        # If token doesn't exist we still return 204 but could log it
        return {"msg": "ok"}
    return {"msg": "logged_out"}
