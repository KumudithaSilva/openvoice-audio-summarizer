from typing import Dict, List

from interfaces.llm.i_ai_client import IAIClient
from interfaces.llm.i_falcon_operations import IFalconAIOperations
from logs.logger_singleton import Logger
from logs.logger_streamlit import LoggerStreamlit


class FalconAIService(IFalconAIOperations):
    """
    Service class for interacting with an AI client.

    Attributes:
        ai_client (IAIClient): Abstract AI client.
        client (FalconAI): FalconAI client instance.
        logger (Logger): Logger instance for info and error messages.
        logger_streamlit (LoggerStreamlit, optional): Streamlit logger instance.
    """

    def __init__(self, ai_client: IAIClient, logger=None, logger_streamlit=None):
        """
        Initialize FlaconAIService with AI client and prompt provider.

        Args:
            ai_client (IAIClient): Abstract AI client.
            logger (Logger, optional): Logger instance. Defaults to Logger singleton.
            logger_streamlit (LoggerStreamlit, optional): Streamlit logger instance.
        """
        self.ai_client = ai_client
        self.logger = logger or Logger(self.__class__.__name__)
        self.logger_streamlit = logger_streamlit or LoggerStreamlit()

    def create_response(self, messages: List[Dict]) -> str:
        """
        Generate response for client request

        Args:
            messages: List[Dict] : List of messages

        Returns:
            str: Generated response in text.
        """
        try:
            self.logger.info("Sending client request to FalconAI API...")
            self.logger_streamlit.add("Summary Generation Started")
            # Create chat completion request
            response = self.ai_client.chat_completions_create(messages=messages)
            self.logger.info("Received response from FalconAI API.")
            self.logger_streamlit.add("Summary Generation Completed")
            return response

        except Exception as e:
            self.logger.error(f"Falcon AI error: {e}")
            return "Error: Failed to generate response."
