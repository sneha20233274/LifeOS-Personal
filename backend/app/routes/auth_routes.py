# backend/app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError
from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserOut,UserLogin
from app.schemas.token import TokenOut, TokenRefresh
from app.crud.user_crud import create_user, get_user_by_email, save_refresh_token, revoke_refresh_token, is_refresh_token_revoked, get_user
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token,get_current_user,hash_password
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import ChangePasswordRequest


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
    try:
        decoded = decode_token(payload.refresh_token)

        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        jti = decoded.get("jti")
        if is_refresh_token_revoked(db, jti):
            raise HTTPException(status_code=401, detail="Token revoked")

        user_id = decoded.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # issue new access token
    access = create_access_token(subject=str(user_id))

    return TokenOut(
        access_token=access,
        refresh_token=payload.refresh_token,  # unchanged (no rotation)
    )


@router.post("/logout", status_code=204)
def logout(payload: TokenRefresh, db: Session = Depends(get_db)):
    print("🚪 ===== LOGOUT REQUEST RECEIVED =====")

    try:
        decoded = decode_token(payload.refresh_token)
        print("🔓 Refresh token decoded:", decoded)

        jti = decoded.get("jti")
        user_id = decoded.get("sub")

        print(f"👤 User ID: {user_id}")
        print(f"🆔 Refresh Token JTI: {jti}")

        if jti:
            revoke_refresh_token(db, jti)
            print("✅ Refresh token successfully revoked in DB")

        else:
            print("⚠️ No JTI found in token")

    except JWTError as e:
        print("⚠️ Logout called with invalid/expired refresh token")
        print("JWT Error:", str(e))
        print("✅ Still treating logout as successful")

    print("🏁 ===== LOGOUT COMPLETED =====")
    return


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ verify current password
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # 2️⃣ confirm new password
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # 3️⃣ prevent reuse
    if verify_password(payload.new_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="New password must be different")

    # 4️⃣ update password
    current_user.password_hash = hash_password(payload.new_password)


    # 5️⃣ revoke all refresh tokens (VERY IMPORTANT)
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.user_id
    ).update({"revoked": True})

    db.commit()

    return {"message": "Password updated successfully"}



