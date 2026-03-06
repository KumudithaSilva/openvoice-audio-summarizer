from typing import Dict, List

from interfaces.chat.i_chat_history import IMessageCompletionService
from interfaces.chat.i_oneshot_prompt import IPrompt
from logs.logger_singleton import Logger


class MessageCompletionService(IMessageCompletionService):
    """
    Handling chat messages
    """

    def __init__(self, prompt_provider: IPrompt, logger=None):
        """
        Initialize Chat messages with injected dependencies.

        Args:
            logger (Logger, optional): Logger instance.
            prompt_provider (IPrompt): Prompt provider implementation.
        """
        self.logger = logger or Logger(self.__class__.__name__)
        self.prompt_provider = prompt_provider
        self.chat_messages: List[Dict] = []

    def initialize(self, voice_text: str) -> List[Dict]:
        """
        Initialize chat messages with system prompt and userprompt.
        """

        self.chat_messages = [
            {"role": "system", "content": self.prompt_provider.system_prompt()},
            {"role": "user", "content": self.prompt_provider.user_prompt(voice_text)},
        ]

        self.logger.info("Initial chat history created")

        return self.chat_messages
