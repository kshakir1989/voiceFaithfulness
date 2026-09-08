"""Local Faster-Whisper STT; marks unavailable if torch/package missing."""

from __future__ import annotations

from pathlib import Path

from app.providers.errors import ProviderError


class LocalFasterWhisperSTT:
    def __init__(self) -> None:
        self.agent_id = "local-faster-whisper"
        self._model = None
        self.available = True
        try:
            from faster_whisper import WhisperModel  # type: ignore

            # Tiny model keeps free-tier local demos light.
            self._model = WhisperModel("tiny", device="cpu", compute_type="int8")
        except Exception:
            self.available = False
            self._model = None

    async def transcribe(self, audio_path: str) -> str:
        if not self.available or self._model is None:
            raise ProviderError(
                "provider_error",
                "Local Faster-Whisper is unavailable (install faster-whisper and torch).",
            )
        path = Path(audio_path)
        if not path.is_file():
            raise ProviderError("invalid_audio", f"Audio not found: {audio_path}")
        segments, _info = self._model.transcribe(str(path))
        text = " ".join(seg.text.strip() for seg in segments).strip()
        if not text:
            raise ProviderError("provider_error", "Local STT produced an empty transcript.")
        return text
