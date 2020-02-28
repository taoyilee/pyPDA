import itertools
from collections import deque
from typing import Tuple

import numpy as np

from pypda.wavelets import Waveform, TriangGaussian


class PulseModelRaw(Waveform):
    def __init__(self, samples:int=100, baseline=80, pulse_amplitudes: Tuple = (8, 3, 4, 2, 1),
                 delta_time: Tuple = (10, 10, 10, 10),
                 triangle_m: Tuple = (20, 20, 20, 20, 20),
                 gaussian_m: Tuple = (16, 16, 16, 16, 16),
                 gaussian_std: Tuple = (2, 2, 2, 2, 2)):
        assert len(delta_time) == len(pulse_amplitudes) - 1, "len(delta_time) must be len(pulse_heights) - 1"
        assert len(triangle_m) == len(pulse_amplitudes), "len(triangle_m) must be len(pulse_heights)"
        assert len(gaussian_m) == len(pulse_amplitudes), "len(gaussian_m) must be len(pulse_heights)"
        assert len(gaussian_std) == len(pulse_amplitudes), "len(gaussian_std) must be len(pulse_heights)"
        self.baseline = baseline
        self.samples = samples
        self.wavelets = [TriangGaussian(amplitude=am, triang_m=tm, gaussian_m=gm, gaussian_std=gs)
                         for am, tm, gm, gs in zip(pulse_amplitudes, triangle_m, gaussian_m, gaussian_std)]
        deque(map(lambda w, delta: w.shift(delta), self.wavelets[1:], itertools.accumulate(delta_time)))

    @property
    def waveform(self) -> np.ndarray:
        from scipy import signal
        if self._waveform is None:
            self._waveform = sum(self.wavelets).waveform + self.baseline
            self._waveform = signal.resample(self._waveform, self.samples)
        return self._waveform
