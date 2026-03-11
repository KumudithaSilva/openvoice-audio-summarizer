from abc import ABC, abstractmethod
from dto.audio_data import AudioData


class IWhisperOperations(ABC):

    @abstractmethod
    def create_transcription(
        self, audio: AudioData, model: str = "whisper-medium-en"
    ) -> str:
        """
        Transcribe audio into text.

        Args:
            audio: AudioData object containing waveform and sample rate.
            model: Name of the Whisper model to use.

        Returns:
            str: The transcribed text.
        """
        pass
