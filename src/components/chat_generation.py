from typing import Dict, List


from interfaces.chat.i_text_generation import ITextGenereateService
from interfaces.llm.i_falcon_operations import IFalconAIOperations


class ChatGenerationService(ITextGenereateService):
    """
    Initializes FalconAI chat using interface-based dependencies.

    Attributes:
        falcon_ai_service (IOpenAIOperations): Interface for AI operations.
        tool_schema (IToolSchema): Interface for tool schema generation.
    """

    def __init__(self, falcon_ai_service: IFalconAIOperations):
        """
        Initialize the ChatCompletionService.

        Args:
            falcon_ai_service (IFalconAIOperations): Interface for AI operations.
        """
        self.falcon_ai_service: IFalconAIOperations = falcon_ai_service

    def generate(self, messages: List[Dict]) -> str:
        """
        Generate a response for the client request.

        Args:
            messages (List[Dict]): List of chat messages.

        Returns:
            str: Return response from AI
        """
        return self.falcon_ai_service.create_response(messages=messages)
