from abc import ABC, abstractmethod
from ast import Dict
from typing import List


class IFalconAIOperations(ABC):

    @abstractmethod
    def create_response(
        self, messages: List[Dict], model: str = "Falcon3-1B-Instruct"
    ) -> str:
        pass
