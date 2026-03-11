from abc import ABC, abstractmethod
from typing import List


class IUiLogger(ABC):
    """
    interface for streamlit ui logger.
    """

    @abstractmethod
    def add(self, message: str) -> None:
        pass

    @abstractmethod
    def fetch(self) -> List[str]:
        pass

    @abstractmethod
    def empty(self) -> None:
        """
        Clear all messages from the logger.
        """
        pass
