"""Speech-to-text helper using OpenAI Whisper (local model)."""
from __future__ import annotations
import os
import tempfile
import hashlib
import requests
import whisper

MODEL_NAME = os.getenv("WHISPER_MODEL", "small")
_whisper_model = None

def _load_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(MODEL_NAME)
    return _whisper_model


def _download_file(url: str) -> str:
    """Download remote audio file to a temp path and return the path."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    suffix = os.path.splitext(url)[1] or ".wav"
    # Use hash to avoid duplicates
    h = hashlib.sha1(url.encode()).hexdigest()[:10]
    temp_path = os.path.join(tempfile.gettempdir(), f"twilio_recording_{h}{suffix}")
    with open(temp_path, "wb") as f:
        f.write(resp.content)
    return temp_path


def transcribe_audio(url: str) -> str:
    """Given a RecordingUrl from Twilio, return transcribed text."""
    audio_path = _download_file(url + ".wav")  # ensure .wav extension
    model = _load_model()
    result = model.transcribe(audio_path, language="en")
    return result.get("text", "")
