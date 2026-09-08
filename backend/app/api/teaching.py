"""Teach-in-UI copy for the five pipeline concepts."""

from fastapi import APIRouter

from app.domain.teaching import MESSAGES

router = APIRouter(tags=["teaching"])


@router.get("/teaching/messages")
def teaching_messages() -> dict:
    return {"messages": MESSAGES}
