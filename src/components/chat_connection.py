from typing import Optional

from infrastructure.falcon_client import FalconAIClientWrapper
from interfaces.chat.i_chatbot_connection import IChatConnection
from interfaces.infra.i_config_provider import IConfigProvider
from interfaces.llm.i_ai_client import IAIClient


class ChatConnectionService(IChatConnection):
    """
    Initializes AI chatbot connection using interface-based dependencies.
    """

    def __init__(self, config_provider: IConfigProvider):
        """
        Initialize ChatConnectionService.

        Args:
            config_provider (IConfigProvider): Interface to obtain model details.
        """
        self.config_provider = config_provider
        self.client: Optional[IAIClient] = None

    def connect(self) -> IAIClient:
        """
        Create and return the FalconAI client. Only creates it once per instance.

        Returns:
            IAIClient: Interface for AI client operations.
        """
        if self.client is None:
            self.client = FalconAIClientWrapper(self.config_provider)
        return self.client
