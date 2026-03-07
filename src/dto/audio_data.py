from dataclasses import dataclass
import torch


@dataclass
class AudioData:
    waveform: torch.Tensor
    sample_rate: int
