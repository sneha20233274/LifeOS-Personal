# backend/app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException,Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserOut
from app.crud.user_crud import get_user
from app.core.security import decode_token
from jose import JWTError
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserProfileUpdate

router = APIRouter(tags=["Users"])



def get_current_user_from_bearer(authorization: str | None, db: Session):
    # Expect header Authorization: Bearer <token>
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Token is not access token")
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@router.put("/me")
def update_my_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
   if payload.username is not None:
    # only check uniqueness if username actually changed
    if payload.username != current_user.username:
        existing = (
            db.query(User)
            .filter(
                User.username == payload.username,
                User.user_id != current_user.user_id
            )
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

        current_user.username = payload.username


    if payload.first_name is not None:
        current_user.first_name = payload.first_name

    if payload.middle_name is not None:
        current_user.middle_name = payload.middle_name

    if payload.last_name is not None:
        current_user.last_name = payload.last_name

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "user_id": current_user.user_id,
            "username": current_user.username,
            "first_name": current_user.first_name,
            "middle_name": current_user.middle_name,
            "last_name": current_user.last_name,
            "email_id": current_user.email_id,
        },
    }
@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "middle_name": current_user.middle_name,
        "last_name": current_user.last_name,
        "email_id": current_user.email_id,
        "timezone": current_user.timezone,
        "created_at":current_user.created_at
    } 
