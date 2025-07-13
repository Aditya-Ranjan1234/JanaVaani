from __future__ import annotations
from typing import Dict, Any
import os, sys
from pathlib import Path

parent = Path(__file__).resolve().parent.parent
if str(parent) not in sys.path:
    sys.path.append(str(parent))

from agents.base import BaseAgent  # noqa: E402
from scheme_finder import find_schemes  # noqa: E402
from translator import translate_text  # noqa: E402


class AgricultureAgent(BaseAgent):
    """Handles farmer-centric queries and recommends schemes."""

    def handle(self, user_text: str, context: Dict[str, Any] | None = None) -> str:  # noqa: D401
        user_en = translate_text(user_text, target_language="en")
        schemes = find_schemes(user_en)
        if not schemes:
            return (
                "I could not find a specific government scheme for your issue right now. Please "
                "contact your local agriculture officer or Krishi Vigyan Kendra for assistance."
            )

        lines = [
            "Here are some government agriculture schemes that could help you:" ,
        ]
        for row in schemes:
            lines.append(f"- {row['Scheme']}: {row['Description']} (Contact: {row['Contact']})")

        return "\n".join(lines)
