from abc import ABC, abstractmethod
from typing import IO, Union


class IVoiceTranscriptionService(ABC):
    """
    Interface transcription generation.
    """

    @abstractmethod
    def generate(self, audio_path: Union[str, IO[bytes]]) -> str:
        """
        Genereate transcription for client request

        Args:
            audio_path (str | IO[bytes]): Path to audio file or file-like object.

        Returns:
            str: Return response for AI
        """
        pass
