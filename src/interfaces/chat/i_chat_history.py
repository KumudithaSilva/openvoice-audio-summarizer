from abc import ABC, abstractmethod
from typing import Dict, List


class IMessageCompletionService(ABC):
    """
    Interface for managing chat details.
    """

    @abstractmethod
    def initialize(self, voice_text: str) -> List[Dict]:
        """Full Chat list of system and user"""
        pass
