# backend/app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException,Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserOut
from app.crud.user_crud import get_user
from app.core.security import decode_token
from jose import JWTError
from app.utils.oauth2_scheme  import swagger_bearer_auth

router = APIRouter(tags=["users"],dependencies=[Depends(swagger_bearer_auth)])

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

@router.get("/account/me", response_model=UserOut)
def read_current_user(authorization: str | None = Header(None), db: Session = Depends(get_db)):
    # FastAPI automatically injects header if you name param `authorization: str = Header(None)`
    # To keep it simple we retrieve from function arg.
    user = get_current_user_from_bearer(authorization, db)
    return user
