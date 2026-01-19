from google.oauth2.credentials import Credentials
from sqlalchemy.orm import Session
from app.models.google_token import GoogleToken


def get_credentials_for_user(db: Session, user_id: int) -> Credentials | None:
    token = (
        db.query(GoogleToken)
        .filter(GoogleToken.user_id == user_id)
        .first()
    )

    if not token:
        return None

    return Credentials(
        token=token.access_token,
        refresh_token=token.refresh_token,
        token_uri=token.token_uri,
        client_id=token.client_id,
        client_secret=token.client_secret,
        scopes=token.scopes.split(" "),
    )
