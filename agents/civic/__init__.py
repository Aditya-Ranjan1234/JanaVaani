from __future__ import annotations
from typing import Dict, Any
from agents.base import BaseAgent

import requests

# Simplified placeholder for civic authority endpoint
def send_civic_complaint(description: str, location: str | None = None):
    # TODO: integrate with real civic APIs / email service
    print(f"[CIVIC] Complaint logged: {description} at {location}")


class CivicAgent(BaseAgent):
    """Handles civic complaints like potholes, garbage, etc."""

    KEYWORDS = [
        "pothole",
        "garbage",
        "trash",
        "cleanliness",
        "sewage",
        "water leak",
        "street light",
    ]

    def handle(self, user_text: str, context: Dict[str, Any] | None = None) -> str:
        # Very naive location capture (could be improved with NER)
        location = context.get("location") if context else None
        if not location:
            return "Please tell me the exact location or landmark of the issue so I can report it."

        send_civic_complaint(user_text, location)
        return (
            f"Your civic issue has been reported to the local authorities for {location}. "
            "You will receive an update soon. Thank you for helping keep our community clean."
        )
