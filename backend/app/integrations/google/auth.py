from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    return creds
