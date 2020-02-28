import numpy as np
from scipy import signal

from .waveform import Waveform


class TriangGaussian(Waveform):
    _waveform = None

    def __init__(self, baseline=0, amplitude=1, triang_m=20, gaussian_m=16, gaussian_std=2):
        self.amplitude = amplitude
        self.baseline = baseline
        self.triang_m = triang_m
        self.gaussian_m = gaussian_m
        self.gaussian_std = gaussian_std

        self.triangle = signal.triang(triang_m)
        self.gaussian = signal.gaussian(gaussian_m, std=gaussian_std)

    @property
    def waveform(self) -> np.ndarray:
        if self._waveform is None:
            self._waveform = self.baseline + self.amplitude * signal.convolve(self.triangle, self.gaussian)
        return self._waveform

    def __len__(self):
        return len(self.waveform)
