# backend/app/middleware/auth.py

from typing import Iterable, Optional, List
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.utils.token_extract import extract_token
import logging

logger = logging.getLogger("app.auth")


# -------------------------
# Helpers (UNCHANGED)
# -------------------------

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

        if raw.endswith("$"):  # exact match
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


# -------------------------
# Middleware (FIXED)
# -------------------------

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, protected: Optional[Iterable[str]] = None):
        super().__init__(app)
        self.protected_paths: List[str] = list(protected or [])

    async def dispatch(self, request: Request, call_next):
        # 🔥 CRITICAL FIX — ALLOW CORS PREFLIGHT
        if request.method == "OPTIONS":
            return await call_next(request)

        request.state.user = None
        path = request.scope.get("path", "/")

        # 🔹 Skip auth for unprotected paths
        if not _is_path_protected(path, self.protected_paths):
            return await call_next(request)

        # 🔹 Extract token
        token_raw = extract_token(request)
        if not token_raw:
            logger.debug("AuthMiddleware: missing token (path=%s)", path)
            return JSONResponse(
                {"detail": "Missing authentication token"},
                status_code=401,
            )

        # 🔹 Handle "Bearer <token>"
        if token_raw.lower().startswith("bearer "):
            token = token_raw.split(" ", 1)[1]
        else:
            token = token_raw

        # 🔹 Verify JWT
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as exc:
            logger.debug("AuthMiddleware: invalid token: %s", exc)
            return JSONResponse(
                {"detail": "Invalid or expired token"},
                status_code=401,
            )

        # 🔹 Attach payload
        request.state.user = payload

        return await call_next(request)
