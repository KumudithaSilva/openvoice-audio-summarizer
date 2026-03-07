from dto.audio_data import AudioData
from interfaces.audio.i_audio_processor import IAudioProcessor
from logs.logger_singleton import Logger
import torchaudio


class AudioProcessor(IAudioProcessor):
    """
    Provide preprocess audio waveform.
    """

    def __init__(self, logger=None):
        """
        Initialize the Audio processor instance.

        Args:
            logger (Logger, optional): Logger instance. If None, a default is used.
        """
        self.logger = logger or Logger(self.__class__.__name__)
        self.audio_data: AudioData | None = None

    def load_audio_file(self, path: str) -> AudioData:
        """
        Load audio file and return AudioData containing waveform and sample rate.

        Args:
            path (str): Path to audio file.

        Returns:
            AudioData: Loaded audio data.

        Raises:
            FileNotFoundError: If the audio file does not exist.
            RuntimeError: If loading fails for any reason.
        """
        try:
            waveform, sample_rate = torchaudio.load(path)
            self.audio_data = AudioData(waveform=waveform, sample_rate=sample_rate)
            self.logger.info(
                f"Audio file loaded: {path}, shape={waveform.shape}, sample_rate={sample_rate}"
            )
            return self.audio_data

        except FileNotFoundError as fnf_error:
            self.logger.error(f"File not found: {path}")
            raise fnf_error

        except Exception as e:
            self.logger.error(f"Failed to load audio file {path}: {e}")
            raise RuntimeError(f"Failed to load audio file {path}") from e

    def preprocess_audio(self, samplerate: int = 16000) -> AudioData:
        """
        Preprocess the stored audio waveform and samplerate.

        Returns:
            AudioData: Processed audio data.

        Raises:
            ValueError: If no audio has been loaded yet.
            RuntimeError: If preprocessing fails.
        """
        if self.audio_data is None:
            self.logger.error("No audio loaded.")
            raise ValueError("No audio loaded.")

        try:
            # Convert to mono if more than 1 channel
            if self.audio_data.waveform.shape[0] > 1:
                self.audio_data.waveform = self.audio_data.waveform.mean(
                    dim=0, keepdim=True
                )
                self.logger.info(f"Converted audio to mono.")

            # Resample the waveform
            if self.audio_data.sample_rate != samplerate:
                resampler = torchaudio.transforms.Resample(
                    orig_freq=self.audio_data.sample_rate, new_freq=samplerate
                )

                self.audio_data.waveform = resampler(self.audio_data.waveform)
                self.audio_data.sample_rate = samplerate

                self.logger.info(f"Resampled audio data")

            return self.audio_data

        except Exception as e:
            self.logger.error(f"Failed to preprocess audio: {e}")
            raise RuntimeError("Audio preprocessing failed") from e


if __name__ == "__main__":
    processor = AudioProcessor()

    audio = processor.load_audio_file("meeting_audio.wav")
    audio = processor.preprocess_audio(samplerate=16000)

    print(audio.waveform)
