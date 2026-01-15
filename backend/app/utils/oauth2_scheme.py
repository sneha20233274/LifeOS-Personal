# app/utils/dependencies.py
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def swagger_bearer_auth(token: str = Depends(oauth2_scheme)):
    pass
