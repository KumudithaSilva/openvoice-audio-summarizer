from interfaces.chat.i_oneshot_prompt import IPrompt
from logs.logger_singleton import Logger


class PromptProvider(IPrompt):
    """
    Provider system prompts for one-shot learning tasks.
    """

    def __init__(self, logger=None):
        """
        Initialize the PromptProvider instance.

        Args:
            logger (Logger, optional): A logger instance. If None, a
                default logger is created using the class name.
        """
        self.logger = logger or Logger(self.__class__.__name__)

    def system_prompt(self) -> str:
        """
        Get the system prompt.

        Returns:
            str: The system prompt string.
        """
        system_prompt = """You produce minutes of meetings from transcripts, with summary, 
        key discussion points,takeaways and action items with owners, in markdown format without code blocks.
        """
        return system_prompt

    def user_prompt(self, voice_text: str) -> str:
        """
        Get the user prompt.

        Returns:
            str: The user prompt string.
        """
        user_prompt = f"""
        Below is an extract transcript of a meeting.
        Please write minutes in markdown without code blocks, including:
        - a summary with attendees, location and date if available
        - discussion points if available
        - takeaways if available
        - action items with owners if available

        Do not add anyting that not in the context

        Transcription:
        {voice_text}
        """
        return user_prompt
