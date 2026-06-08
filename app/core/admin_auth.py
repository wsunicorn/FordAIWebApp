from __future__ import annotations

import base64
import hashlib
import hmac
import time
from urllib.parse import quote

from fastapi import HTTPException, Request, status

from app.core.config import settings

ADMIN_SESSION_COOKIE = "ford_admin_session"


def _signature(payload: str) -> str:
    return hmac.new(
        settings.secret_key.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_admin_credentials(username: str, password: str) -> bool:
    username_ok = hmac.compare_digest(username, settings.admin_username)
    password_ok = hmac.compare_digest(password, settings.admin_password)
    return username_ok and password_ok


def create_admin_session(username: str) -> str:
    expires_at = int(time.time()) + settings.admin_session_ttl_seconds
    payload = f"{username}|{expires_at}"
    signed_payload = f"{payload}|{_signature(payload)}"
    return base64.urlsafe_b64encode(signed_payload.encode("utf-8")).decode("ascii")


def verify_admin_session(cookie_value: str | None) -> str | None:
    if not cookie_value:
        return None

    try:
        decoded = base64.urlsafe_b64decode(cookie_value.encode("ascii")).decode("utf-8")
        username, expires_at_raw, signature = decoded.rsplit("|", 2)
        payload = f"{username}|{expires_at_raw}"
        expires_at = int(expires_at_raw)
    except (ValueError, UnicodeDecodeError):
        return None

    if expires_at < int(time.time()):
        return None

    if not hmac.compare_digest(signature, _signature(payload)):
        return None

    if not hmac.compare_digest(username, settings.admin_username):
        return None

    return username


def require_admin(request: Request) -> str:
    username = verify_admin_session(request.cookies.get(ADMIN_SESSION_COOKIE))
    if username:
        return username

    next_path = quote(str(request.url.path), safe="/")
    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        headers={"Location": f"/admin/login?next={next_path}"},
    )
