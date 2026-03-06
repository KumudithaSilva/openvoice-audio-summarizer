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
        Initialize OpenAI client wrapper.

        Args:
            config_provider (IConfigProvider): Interface to obtain model details.
        """
        self.config_provider = config_provider.get_model_details()
        self.client = Falcon(self.config_provider)

    def chat_completions_create(
        self, messages: List[Dict], model: str = "Falcon3-1B-Instruct"
    ) -> str:
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


if __name__ == "__main__":
    from infrastructure.config_provider import ConfigProvider

    cp = ConfigProvider()
    falcon = FalconAIClientWrapper(config_provider=cp)

    messages = [
        {
            "role": "system",
            "content": "\nYou produce summary key discussion points,in markdown format without code blocks.\n",
        },
        {
            "role": "user",
            "content": "\nBelow is an extract transcript of a meeting: \nHello, how are you? We are planning to conduct our Annual next meeting on 24th February 2026 at 4 pm at Main Auditorium.\n",
        },
    ]

    result = falcon.chat_completions_create(messages)
    print(result)
