from abc import ABC, abstractmethod

from infrastructure.falcon_client import FalconAIClientWrapper


class IChatConnection(ABC):
    """
    Interface for initializing AI chatbot connection.
    """

    @abstractmethod
    def connect(self) -> FalconAIClientWrapper:
        """
        Initializing AI chatbot converstion.

        Returns:
            FalconAIClientWrapper: Concrete wrapper for the FalconAI
        """
        pass
