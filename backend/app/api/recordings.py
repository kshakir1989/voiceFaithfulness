"""List, upload, and stream recordings for picker + preview."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse

from app.domain.recordings import (
    APP_ROOT,
    find_recording,
    list_recordings,
    purge_session_uploads,
    resolve_audio_file,
    session_upload_dir,
)
from app.domain.session import get_or_set_session_id, read_session_id
from app.domain.store import store
from app.policy.all_ages import is_all_ages_eligible, validate_audio_meta

router = APIRouter(tags=["recordings"])

ALLOWED_SUFFIXES = {".wav", ".mp3", ".m4a", ".ogg", ".webm", ".flac"}


@router.get("/recordings")
def get_recordings(request: Request, response: Response) -> dict:
    sid = get_or_set_session_id(request, response)
    return {
        "recordings": list_recordings(sid),
        "session_ephemeral_uploads": True,
        "upload_retention": "session_only",
    }


@router.get("/recordings/{recording_id}/audio")
def get_recording_audio(recording_id: str, request: Request, response: Response) -> FileResponse:
    sid = get_or_set_session_id(request, response)
    rec = find_recording(recording_id, sid)
    if not rec:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Recording not found."})
    path = resolve_audio_file(rec)
    if path is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Audio file missing."})
    media = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return FileResponse(path, media_type=media, filename=path.name)


@router.post("/recordings/upload", status_code=201)
async def upload_recording(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    title: Optional[str] = Form(default=None),
) -> dict:
    sid = get_or_set_session_id(request, response)
    raw_name = file.filename or "upload.wav"
    suffix = Path(raw_name).suffix.lower() or ".wav"
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_audio", "message": f"Unsupported file type: {suffix}"},
        )
    data = await file.read()
    ok, msg = validate_audio_meta(size_bytes=len(data), content_type=file.content_type)
    if not ok:
        raise HTTPException(status_code=400, detail={"code": "invalid_audio", "message": msg or "Invalid audio."})

    display_title = (title or Path(raw_name).stem or "Local recording").strip()
    if not is_all_ages_eligible(title=display_title, transcript=""):
        raise HTTPException(
            status_code=403,
            detail={
                "code": "all_ages_blocked",
                "message": "This recording is not all-ages eligible and cannot be scored.",
            },
        )

    recording_id = f"local-{uuid4().hex[:12]}"
    dest = session_upload_dir(sid) / f"{recording_id}{suffix}"
    dest.write_bytes(data)

    rec = {
        "id": recording_id,
        "title": f"{display_title} (session only)",
        "source_type": "local",
        "audio_path": str(dest.resolve()),
        "duration_seconds": None,
        "all_ages_eligible": True,
        "session_id": sid,
    }
    store.add_local_recording(sid, rec)

    return {
        "id": rec["id"],
        "title": rec["title"],
        "source_type": rec["source_type"],
        "duration_seconds": rec["duration_seconds"],
        "all_ages_eligible": True,
        "ephemeral": True,
        "audio_url": f"/api/recordings/{rec['id']}/audio",
    }


@router.delete("/recordings/session")
def delete_session_uploads(request: Request) -> dict:
    """Drop this browser session's uploads (tab close / explicit clear)."""
    sid = read_session_id(request)
    if not sid:
        return {"ok": True, "cleared": 0}
    purge_session_uploads(sid)
    return {"ok": True, "cleared": 1}
