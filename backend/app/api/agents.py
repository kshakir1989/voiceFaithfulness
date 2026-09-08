"""STT and judge drop-down catalogs (IDs locked in research.md)."""

from fastapi import APIRouter

from app.providers.catalog import judge_catalog, transcription_catalog

router = APIRouter(tags=["agents"])


@router.get("/agents/transcription")
def get_transcription_agents() -> dict:
    return transcription_catalog()


@router.get("/agents/judge")
def get_judge_agents() -> dict:
    return judge_catalog()
