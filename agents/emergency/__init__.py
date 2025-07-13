from __future__ import annotations
from typing import Dict, Any
from agents.base import BaseAgent
from messaging import send_sms_summary

EMERGENCY_NUMBERS = {
    "police": "100",
    "ambulance": "102",
    "fire": "101",
    "women": "1091",
    "disaster": "108",
}


def dial_emergency(service: str, caller: str, details: str):
    # Placeholder: Here you'd integrate outbound call API from Twilio
    number = EMERGENCY_NUMBERS.get(service)
    print(f"[EMERGENCY] Dialling {service} ({number}) for caller {caller}: {details}")
    # Also send SMS confirmation
    if caller:
        send_sms_summary(
            f"Your emergency request for {service.upper()} has been forwarded to {number}. Help is on the way.",
            caller,
        )


class EmergencyAgent(BaseAgent):
    """Detects emergencies and calls appropriate services."""

    SERVICE_KEYWORDS = {
        "police": ["theft", "violence", "robbery", "assault"],
        "ambulance": ["injury", "accident", "medical", "unconscious"],
        "fire": ["fire", "burning", "smoke"],
        "women": ["harassment", "stalking", "molestation"],
    }

    def _detect_service(self, text: str) -> str | None:
        text = text.lower()
        for service, keywords in self.SERVICE_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return service
        return None

    def handle(self, user_text: str, context: Dict[str, Any] | None = None) -> str:
        service = self._detect_service(user_text)
        caller = context.get("caller_number") if context else None
        if not service:
            return "Please describe your emergency so I can connect you to the correct service (police, ambulance, fire)."
        dial_emergency(service, caller, user_text)
        return f"Connecting you to {service.capitalize()} services now. Stay calm; help is on the way."
