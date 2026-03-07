from abc import ABC, abstractmethod
from dto.audio_data import AudioData


class IAudioProcessor(ABC):
    
    @abstractmethod
    def load_audio_file(self, path: str) -> AudioData:
        pass

    @abstractmethod
    def preprocess_audio(self, samplerate: int = 16000) -> AudioData:
        pass