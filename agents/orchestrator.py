from __future__ import annotations
from typing import Dict, Any
import re

from agents.agriculture import AgricultureAgent
from agents.civic import CivicAgent
from agents.emergency import EmergencyAgent

AGRI_KEYWORDS = [
    "crop",
    "farmer",
    "agriculture",
    "yield",
    "seed",
    "soil",
    "irrigation",
]

CIVIC_KEYWORDS = CivicAgent.KEYWORDS  # reuse list from agent

EMERGENCY_KEYWORDS = sum(EmergencyAgent.SERVICE_KEYWORDS.values(), [])


class AgentOrchestrator:
    """Routes user utterances to the appropriate domain agent."""

    def __init__(self):
        self.agri_agent = AgricultureAgent()
        self.civic_agent = CivicAgent()
        self.emergency_agent = EmergencyAgent()

    def route(self, user_text: str, context: Dict[str, Any] | None = None) -> str:
        lowered = user_text.lower()

        if any(re.search(rf"\b{kw}\b", lowered) for kw in EMERGENCY_KEYWORDS):
            return self.emergency_agent.handle(user_text, context)

        if any(re.search(rf"\b{kw}\b", lowered) for kw in AGRI_KEYWORDS):
            return self.agri_agent.handle(user_text, context)

        if any(kw in lowered for kw in CIVIC_KEYWORDS):
            return self.civic_agent.handle(user_text, context)

        # Default fallback
        return (
            "Sorry, I am not sure how to help with that. You can ask about government schemes, "
            "report civic issues, or request emergency assistance."
        )
