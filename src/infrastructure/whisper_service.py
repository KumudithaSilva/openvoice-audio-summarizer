from dto.audio_data import AudioData
from interfaces.llm.i_voice_ai_client import IWhisperClient
from interfaces.llm.i_whisper_operations import IWhisperOperations
from logs.logger_singleton import Logger
from logs.logger_streamlit import LoggerStreamlit


class WhisperAIService(IWhisperOperations):
    """
    Service class for interacting with an WhisperAI client.

    Attributes:
        ai_client (IAIClient): Abstract AI client.
        client (FalconAI): FalconAI client instance.
        logger (Logger): Logger instance for info and error messages.
        logger_streamlit (LoggerStreamlit, optional): Streamlit logger instance.
    """

    def __init__(self, ai_client: IWhisperClient, logger=None, logger_streamlit=None):
        """
        Initialize WhisperAIService with AI.

        Args:
            ai_client (IAIClient): Abstract AI client.
            logger (Logger, optional): Logger instance. Defaults to Logger singleton.
            logger_streamlit (LoggerStreamlit, optional): Streamlit logger instance.
        """
        self.ai_client = ai_client
        self.logger = logger or Logger(self.__class__.__name__)
        self.logger_streamlit = logger_streamlit or LoggerStreamlit()

    def create_transcription(
        self, audio: AudioData, model: str = "whisper-medium-en"
    ) -> str:
        """
        Transcribe audio into text.

        Args:
            audio: AudioData object containing waveform and sample rate.
            model: Name of the Whisper model to use.

        Returns:
            str: Generated response in text.
        """
        try:
            self.logger.info("Sending client request to WhisperAI API...")
            self.logger_streamlit.add("Audio file Transcription Started")
            # Create chat completion request
            response = self.ai_client.create_transcription(audio=audio)
            self.logger.info("Received response from WhisperAI API.")
            self.logger_streamlit.add("Audio file Transcripted")
            return response

        except Exception as e:
            self.logger.error(f"WhisperAI error: {e}")
            return "Error: Failed to generate response."
