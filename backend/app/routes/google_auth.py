from fastapi import Depends, Request,APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.google_token import GoogleToken
from google_auth_oauthlib.flow import Flow
from app.core.security import get_current_user
from app.models.user import User
router = APIRouter(prefix="/auth", tags=["Auth"])

SCOPES = ["https://www.googleapis.com/auth/calendar"]
REDIRECT_URI = "http://localhost:8000/integerations/google/auth/callback"


@router.get("/login")
def google_login():
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent"
    )

    return {"auth_url": auth_url}





@router.get("/callback")
def google_callback(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    user_id = user.user_id
    code = request.query_params.get("code")

    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(code=code)
    creds = flow.credentials

    token = (
        db.query(GoogleToken)
        .filter(GoogleToken.user_id == user_id)
        .first()
    )

    if token:
        token.access_token = creds.token
        token.refresh_token = creds.refresh_token
        token.expiry = creds.expiry
    else:
        token = GoogleToken(
            user_id=user_id,
            access_token=creds.token,
            refresh_token=creds.refresh_token,
            token_uri=creds.token_uri,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scopes=" ".join(creds.scopes),
            expiry=creds.expiry
        )
        db.add(token)

    db.commit()

    return {"message": "Google Calendar connected successfully"}
