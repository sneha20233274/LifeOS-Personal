# app/utils.py
from fastapi import Request
from typing import Optional

def extract_token(request: Request) -> Optional[str]:
    """
    Look for token in:
      1. Authorization header: "Bearer <token>"
      2. Cookies: access_token, token, refresh_token
      3. Query params: token, authorization
    Returns the raw token string (without 'Bearer ') or None.
    """
    # 1) Authorization header
    auth = request.headers.get("authorization")  # headers are case-insensitive
    if auth:
        # return raw header so caller can decide how to strip scheme
        return auth

    # 2) Cookies
    for name in ("access_token", "token", "refresh_token"):
        t = request.cookies.get(name)
        if t:
            return t

    # 3) Query params - accept both 'token' and 'authorization'
    t = request.query_params.get("token") or request.query_params.get("authorization")
    if t:
        return t

    return None
