"""Text-to-speech module using pyttsx3 (offline)."""
from __future__ import annotations
import pyttsx3
import os
import tempfile

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english')

def synthesize_speech(text: str) -> str:
    """Convert text to speech, save to wav, return path."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "msp_tts_output.wav")
    engine.save_to_file(text, file_path)
    engine.runAndWait()
    return file_path
