from abc import ABC, abstractmethod

from infrastructure.whisper_client import WhisperAIClientWrapper


class IWhisperConnection(ABC):
    """
    Interface for initializing Whisper AI audio connection.
    """

    @abstractmethod
    def connect(self) -> WhisperAIClientWrapper:
        """
        Initializing Whisper AI audio.

        Returns:
            WhisperAIClientWrapper: Concrete wrapper for the WhisperAI
        """
        pass
