from typing import Dict, List


from interfaces.chat.i_oneshot_prompt import IPrompt
from interfaces.chat.i_text_generation import ITextGenereateService
from interfaces.llm.i_falcon_operations import IFalconAIOperations


class ChatGenerationService(ITextGenereateService):
    """
    Initializes FalconAI chat using interface-based dependencies.

    Attributes:
        falcon_ai_service (IOpenAIOperations): Interface for AI operations.
    """

    def __init__(
        self, falcon_ai_service: IFalconAIOperations, prompt_provider: IPrompt
    ):
        """
        Initialize the ChatCompletionService.

        Args:
            falcon_ai_service (IFalconAIOperations): Interface for AI operations.
        """
        self.falcon_ai_service: IFalconAIOperations = falcon_ai_service
        self.prompt_provider = prompt_provider
        self.chat_messages: List[Dict] = []

    def generate(self, voice_text: str) -> str:
        """
        Generate a response for the client request.

        Args:
            messages (List[Dict]): List of chat messages.

        Returns:
            str: Return response from AI
        """
        self.chat_messages = [
            {"role": "system", "content": self.prompt_provider.system_prompt()},
            {"role": "user", "content": self.prompt_provider.user_prompt(voice_text)},
        ]
        return self.falcon_ai_service.create_response(messages=self.chat_messages)
