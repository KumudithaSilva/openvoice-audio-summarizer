from abc import ABC, abstractmethod
from typing import List


class IPrompt(ABC):

    @abstractmethod
    def system_prompt(self) -> str:
        pass

    @abstractmethod
    def user_prompt(voice_text: str) -> str:
        pass
