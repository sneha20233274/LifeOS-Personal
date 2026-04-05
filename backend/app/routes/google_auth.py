from fastapi import Depends, Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
import time, json, hmac, hashlib, base64

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import SECRET_KEY
from app.models.google_token import GoogleToken
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = "http://localhost:8000/integrations/google/auth/callback"

import json, hmac, hashlib, base64

def sign_state(data: dict) -> str:
    raw = json.dumps(data).encode()
    sig = hmac.new(
        SECRET_KEY.encode(),
        raw,
        hashlib.sha256
    ).digest()
    return base64.urlsafe_b64encode(raw + b"." + sig).decode()


from urllib.parse import unquote

def verify_state(state: str) -> dict:
    # 🔑 FIX: URL-decode first
    state = unquote(state)

    decoded = base64.urlsafe_b64decode(state.encode())
    raw, sig = decoded.rsplit(b".", 1)

    expected = hmac.new(
        SECRET_KEY.encode(),
        raw,
        hashlib.sha256
    ).digest()

    if not hmac.compare_digest(sig, expected):
        raise HTTPException(status_code=400, detail="Invalid state")

    return json.loads(raw)




@router.get("/login")
def google_login(user: User = Depends(get_current_user)):
    payload = {
        "user_id": user.user_id,
        "ts": int(time.time())
    }

    state = sign_state(payload)

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        state=state
    )

    return {"auth_url": auth_url}


@router.get("/callback")
def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state")

    payload = verify_state(state)

    # Optional expiry check (5 min)
    if time.time() - payload["ts"] > 300:
        raise HTTPException(status_code=400, detail="State expired")

    user_id = payload["user_id"]

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(code=code)
    creds = flow.credentials

    token = db.query(GoogleToken).filter_by(user_id=user_id).first()

    if token:
        token.access_token = creds.token
        token.expiry = creds.expiry
        if creds.refresh_token:
            token.refresh_token = creds.refresh_token
    else:
        db.add(GoogleToken(
            user_id=user_id,
            access_token=creds.token,
            refresh_token=creds.refresh_token,
            token_uri=creds.token_uri,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scopes=" ".join(creds.scopes),
            expiry=creds.expiry
        ))

    db.commit()

    return {"message": "Google Calendar connected successfully"}
