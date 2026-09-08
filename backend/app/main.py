"""Application factory: mounts API routers and CORS for the Vite SPA."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agents, health, metrics, recordings, runs, teaching


def create_app() -> FastAPI:
    app = FastAPI(title="voiceFaithfulness", version="0.1.0")
    # Local Vite dev server only — tighten if you deploy.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix="/api")
    app.include_router(agents.router, prefix="/api")
    app.include_router(recordings.router, prefix="/api")
    app.include_router(runs.router, prefix="/api")
    app.include_router(metrics.router, prefix="/api")
    app.include_router(teaching.router, prefix="/api")
    return app


app = create_app()
