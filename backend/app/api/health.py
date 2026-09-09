"""Liveness probe for local runs and e2e readiness checks."""

from fastapi import APIRouter

from app.domain.mode import providers_mode

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    mode = providers_mode()
    return {
        "status": "ok",
        "providers_mode": mode,
        "providers_label": "stub" if mode == "stub" else "live",
    }
