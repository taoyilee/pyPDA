from collections import deque
from typing import Tuple
import itertools
import numpy as np

from pypda.wavelets import Waveform, TriangGaussian


class PulseModelRaw(Waveform):
    def __init__(self, pulse_amplitudes: Tuple[float] = (8, 3, 4, 2, 1),
                 delta_time: Tuple[int] = (10, 10, 10, 10)):
        assert len(delta_time) == len(pulse_amplitudes) - 1, "len(delta_time) must be len(pulse_heights) - 1"
        self.wavelets = [TriangGaussian(amplitude=amplitude) for i, amplitude in enumerate(pulse_amplitudes)]
        deque(map(lambda w, delta: w.shift(delta), self.wavelets[1:], itertools.accumulate(delta_time)))

    @property
    def waveform(self) -> np.ndarray:
        if self._waveform is None:
            self._waveform = sum(self.wavelets).waveform
        return self._waveform
