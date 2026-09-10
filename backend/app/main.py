"""Application factory: mounts API routers and CORS for the Vite SPA."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agents, demo, dev, health, metrics, recordings, runs, teaching


def create_app() -> FastAPI:
    app = FastAPI(title="voiceFaithfulness", version="0.2.0")
    # Local Vite dev server only — tighten if you deploy.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root() -> dict[str, str]:
        """Avoid a bare 404 when someone opens the API port in a browser."""
        return {
            "message": "voiceFaithfulness API — open the SPA at http://127.0.0.1:5173/",
            "health": "/api/health",
        }

    app.include_router(health.router, prefix="/api")
    app.include_router(agents.router, prefix="/api")
    app.include_router(recordings.router, prefix="/api")
    app.include_router(runs.router, prefix="/api")
    app.include_router(metrics.router, prefix="/api")
    app.include_router(teaching.router, prefix="/api")
    app.include_router(demo.router, prefix="/api")
    app.include_router(dev.router, prefix="/api")
    return app


app = create_app()
