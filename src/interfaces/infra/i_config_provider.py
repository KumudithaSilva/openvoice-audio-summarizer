from abc import ABC, abstractmethod


class IConfigProvider(ABC):

    @abstractmethod
    def get_model_details(self) -> str:
        pass
