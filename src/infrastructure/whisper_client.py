from dto.audio_data import AudioData
from interfaces.infra.i_config_provider import IConfigProvider
from interfaces.llm.i_voice_ai_client import IWhisperClient
from models.whisper_model import Whisper


class WhisperAIClientWrapper(IWhisperClient):
    """
    Concrete wrapper for the Whisper Python library.

    Attributes:
        config_provider (str): model location obtained from IConfigProvider.
        client (WhisperAI): Whisper client instance.
        model (str): Model name to use for audio transcribe generation.
    """

    def __init__(self, config_provider: IConfigProvider):
        """
        Initialize Whisper client wrapper.

        Args:
            config_provider (IConfigProvider): Interface to obtain model details.
        """
        self.config_provider = config_provider.get_model_details(
            model_name="Whisper-Medium"
        )
        self.client = Whisper(self.config_provider)
        self.client.configure_model()

    def create_transcription(self, audio: AudioData) -> str:
        """
        Transcribe an audio waveform into text.

        Args:
            audio: AudioData object containing waveform and sample rate.

        Returns:
            Transcribed text as string.
        """
        response = self.client.create(audio=audio)
        return response
