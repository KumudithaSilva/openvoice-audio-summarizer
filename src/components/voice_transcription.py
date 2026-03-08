from typing import IO, Union

from interfaces.audio.i_audio_processor import IAudioProcessor
from interfaces.chat.i_voice_transcription import IVoiceTranscriptionService
from interfaces.llm.i_whisper_operations import IWhisperOperations


class VoiceTranscriptionService(IVoiceTranscriptionService):
    """
    Initializes WhisperAI using interface-based dependencies.

    Attributes:
        whisper_ai_service (IWhisperOperations): Interface for AI operations.
    """

    def __init__(
        self, whisper_ai_service: IWhisperOperations, audio_processor: IAudioProcessor
    ):
        """
        Initialize the VoiceTranscriptionService.

        Args:
            whisper_ai_service (IWhisperOperations): Interface for AI operations.
            audio_processor (IAudioProcessor) : Interface for preporcess audio.
        """
        self.whisper_ai_service: IWhisperOperations = whisper_ai_service
        self.audio_processor: IAudioProcessor = audio_processor

    def generate(self, audio_path: Union[str, IO[bytes]]) -> str:
        """
        Genereate transcription for client request

        Args:
            audio_path (str | IO[bytes]): Path to audio file or file-like object.

        Returns:
            str: Return response from AI
        """
        self.audio_processor.load_audio_file(path=audio_path)
        processed_audio = self.audio_processor.preprocess_audio()

        processed_audio = self.whisper_ai_service.create_transcription(
            audio=processed_audio
        )

        return processed_audio
