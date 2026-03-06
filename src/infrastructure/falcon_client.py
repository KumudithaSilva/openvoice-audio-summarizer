from typing import Dict, List
from interfaces.llm.i_ai_client import IAIClient
from interfaces.infra.i_config_provider import IConfigProvider
from models.falcon_model import Falcon


class FalconAIClientWrapper(IAIClient):
    """
    Concrete wrapper for the Falcon Python library.

    Attributes:
        config_provider (str): model location obtained from IConfigProvider.
        client (OpenAI): Falcon client instance.
        model (str): Model name to use for chat completions.
    """

    def __init__(self, config_provider: IConfigProvider):
        """
        Initialize Falcon client wrapper.

        Args:
            config_provider (IConfigProvider): Interface to obtain model details.
        """
        self.config_provider = config_provider.get_model_details()
        self.client = Falcon(self.config_provider)
        self.client.configure_model()

    def chat_completions_create(self, messages: List[Dict]) -> str:
        """
        Sends a chat completion request to the AI backend.

        Args:
            messages: List of chat messages
            model: Model name to use.

        Returns:
            The AI-generated response text.
        """
        response = self.client.create(messages=messages)
        return response
