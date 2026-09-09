"""Browser session id for ephemeral uploads (cookie vf_session)."""

from __future__ import annotations

from uuid import uuid4

from fastapi import Request, Response

COOKIE = "vf_session"
MAX_AGE = 60 * 60 * 12  # 12 hours; uploads cleared earlier on tab close when possible


def get_or_set_session_id(request: Request, response: Response) -> str:
    sid = request.cookies.get(COOKIE)
    if sid and len(sid) >= 8:
        return sid
    sid = uuid4().hex
    response.set_cookie(
        key=COOKIE,
        value=sid,
        httponly=True,
        samesite="lax",
        max_age=MAX_AGE,
        path="/",
    )
    return sid


def read_session_id(request: Request) -> str | None:
    sid = request.cookies.get(COOKIE)
    if sid and len(sid) >= 8:
        return sid
    return None
