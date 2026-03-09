from abc import ABC, abstractmethod
from typing import IO, Union


class IVoiceChatService(ABC):
    """
    Interface for an audio to chat response service.
    """

    @abstractmethod
    def generate(self, audio_path: Union[str, IO[bytes]]) -> str:
        """
        Process an audio input and return an AI-generated chat response.

        Args:
            audio_path (str | IO[bytes]): Path to audio file or file-like object.

        Returns:
            str: Return response for AI
        """
        pass
