from abc import ABC, abstractmethod


class ITextGenereateService(ABC):
    """
    Interface text generation.
    """

    @abstractmethod
    def generate(self, voice_text: str) -> str:
        """
        Genereate response for client request

        Returns:
            str: Return response for AI
        """
        pass
