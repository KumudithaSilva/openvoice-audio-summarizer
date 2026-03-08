from abc import ABC, abstractmethod
from typing import Dict, List


class ITextGenereateService(ABC):
    """
    Interface text generation.
    """

    @abstractmethod
    def generate(self, messages: List[Dict]) -> str:
        """
        Genereate response for client request

        Returns:
            str: Return response for AI
        """
        pass
