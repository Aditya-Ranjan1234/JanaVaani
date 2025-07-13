from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Abstract base class for all skill agents."""

    @abstractmethod
    def handle(self, user_text: str, context: Dict[str, Any] | None = None) -> str:  # noqa: D401
        """Return a textual response and optionally perform side-effects.

        context may contain caller_number, location, etc.
        """

    def requires_follow_up(self) -> bool:
        """If the agent still needs more info from the user, override."""
        return False
