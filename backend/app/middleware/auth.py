# backend/app/middleware/auth.py
from typing import Iterable, Optional, List
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.utils.token_extract import extract_token      # should check header/cookies/query
import logging

logger = logging.getLogger("app.auth")

def _normalize_path(p: str) -> str:
    if not p.startswith("/"):
        p = "/" + p
    if p != "/" and p.endswith("/"):
        p = p[:-1]
    return p

def _is_path_protected(path: str, protected_paths: Iterable[str]) -> bool:
    path = _normalize_path(path)
    for raw in protected_paths or []:
        if not raw:
            continue
        raw = raw.strip()
        if raw.endswith("$"):
            cand = _normalize_path(raw[:-1])
            if path == cand:
                return True
            continue
        cand = _normalize_path(raw)
        if path == cand or path.startswith(cand + "/"):
            return True
        if cand == "/":
            return True
    return False

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, protected: Optional[Iterable[str]] = None):
        super().__init__(app)
        self.protected_paths: List[str] = list(protected or [])

    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        path = request.scope.get("path", "/")

        # skip enforcement for unprotected paths
        if not _is_path_protected(path, self.protected_paths):
            return await call_next(request)

        # protected path: extract token
        token_raw = extract_token(request)   # should return header string or cookie/token
        if not token_raw:
            logger.debug("AuthMiddleware: no token found (path=%s)", path)
            # Return 400 as you requested for "token not found"
            return JSONResponse({"detail": "Missing authentication token"}, status_code=400)

        # support "Bearer <token>" or raw token
        if token_raw.lower().startswith("bearer "):
            token = token_raw.split(" ", 1)[1]
        else:
            token = token_raw

        # verify token
        print("veryfying")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as exc:
            logger.debug("AuthMiddleware: token invalid: %s", exc)
            return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)

        # attach payload for handlers
        request.state.user = payload
        return await call_next(request)
