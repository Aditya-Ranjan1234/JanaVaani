"""Simple Google Translate wrapper with fallback to googletrans."""
from __future__ import annotations
import os
from typing import Optional

try:
    from google.cloud import translate_v2 as translate
    gcloud_available = True
except ImportError:
    gcloud_available = False

try:
    from googletrans import Translator as LocalTranslator
    gt_local = LocalTranslator()
except ImportError:
    gt_local = None


def translate_text(text: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    if gcloud_available and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        client = translate.Client()
        result = client.translate(text, target_language=target_language, source_language=source_language)
        return result["translatedText"]
    elif gt_local:
        res = gt_local.translate(text, dest=target_language, src=source_language or "auto")
        return res.text
    return text  # Fallback, no translation
