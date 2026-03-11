from typing import Optional
from infrastructure.whisper_client import WhisperAIClientWrapper
from interfaces.chat.i_whisper_connection import IWhisperConnection
from interfaces.infra.i_config_provider import IConfigProvider
from interfaces.llm.i_voice_ai_client import IWhisperClient


class VoiceConnectionService(IWhisperConnection):
    """
    Initializes WhisperAI connection using interface-based dependencies.
    """

    def __init__(self, config_provider: IConfigProvider):
        """
        Initialize VoiceConnectionService.

        Args:
            config_provider (IConfigProvider): Interface to obtain model details.
        """
        self.config_provider = config_provider
        self.client: Optional[IWhisperClient] = None

    def connect(self) -> IWhisperClient:
        """
        Create and return the WhisperAI client. Only creates it once per instance.

        Returns:
            WhisperAI: Interface for AI client operations.
        """
        if self.client is None:
            self.client = WhisperAIClientWrapper(self.config_provider)
        return self.client
