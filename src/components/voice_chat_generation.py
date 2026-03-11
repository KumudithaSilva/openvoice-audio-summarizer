from typing import IO, Union
from interfaces.chat.i_text_generation import ITextGenereateService
from interfaces.chat.i_voice_chat import IVoiceChatService
from interfaces.chat.i_voice_transcription import IVoiceTranscriptionService


class VoiceChatService(IVoiceChatService):
    """
    Initializes WhisperAI and FalconAI using interface-based dependencies.

    Attributes:
        transcription_service (IVoiceTranscriptionService): Interface for transcription generation.
        chat_service (ITextGenereateService): Interface for text generation.
    """

    def __init__(
        self,
        transcription_service: IVoiceTranscriptionService,
        chat_service: ITextGenereateService,
    ):
        """
        Initialize the VoiceChatService.

        Args:
            falcon_ai_service (IFalconAIOperations): Interface for AI operations.
        """
        self.transcription_service: IVoiceTranscriptionService = transcription_service
        self.chat_service: ITextGenereateService = chat_service

    def generate(self, audio_path: Union[str, IO[bytes]]) -> str:
        """
        Generate a response for the client request.

        Args:
            audio_path (str | IO[bytes]): Path to audio file or file-like object.

        Returns:
            str: Return response from AI
        """
        transcribed_text = self.transcription_service.generate(audio_path)
        generated_response = self.chat_service.generate(voice_text=transcribed_text)

        return generated_response
