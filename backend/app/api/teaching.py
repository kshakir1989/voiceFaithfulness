"""Teach-in-UI copy for the five pipeline concepts."""

from fastapi import APIRouter

from app.domain.teaching import teaching_catalog

router = APIRouter(tags=["teaching"])


@router.get("/teaching/messages")
def teaching_messages() -> dict:
    return teaching_catalog()
