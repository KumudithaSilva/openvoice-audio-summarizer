from abc import ABC, abstractmethod
from typing import IO, Union
from dto.audio_data import AudioData


class IAudioProcessor(ABC):

    @abstractmethod
    def load_audio_file(self, path: Union[str, IO[bytes]]) -> AudioData:
        pass

    @abstractmethod
    def preprocess_audio(self, samplerate: int = 16000) -> AudioData:
        pass
