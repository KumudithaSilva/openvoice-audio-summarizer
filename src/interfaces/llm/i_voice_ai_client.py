from abc import ABC, abstractmethod
from dto.audio_data import AudioData


class IWhisperClient(ABC):
    """
    Abstract interface for a Whisper AI audio transcription client.
    """

    @abstractmethod
    def create_transcription(self, audio: AudioData) -> str:
        """
        Transcribe an audio waveform into text.

        Args:
            audio: AudioData object containing waveform and sample rate.

        Returns:
            Transcribed text as string.
        """
        pass
