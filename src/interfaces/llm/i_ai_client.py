from abc import ABC, abstractmethod
from typing import Dict, List


class IAIClient(ABC):
    """
    Abstract interface for an AI client.
    """

    @abstractmethod
    def chat_completions_create(
        self, messages: List[Dict], model: str = "Falcon3-1B-Instruct"
    ) -> str:
        """
        Sends a chat completion request to the AI backend.

        Args:
            messages: List of chat messages
            model: Model name to use.

        Returns:
            The AI-generated response text.
        """
        pass
