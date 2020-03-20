from collections import deque
from itertools import accumulate

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import cheby2, sosfiltfilt

from pypda.hmm import HMM
from pypda.parameters import PulseWaveParameters
from pypda.pulse_model import PulseModelRaw
from pypda.wavelets import ArbitraryWaveform


class PulseWave:
    @property
    def beats(self):
        return np.ceil(self.bpm * self.length / 60).astype(int) + 1

    @property
    def beat_period(self):
        return 1 / (self.bpm / 60)  # in seconds

    def __init__(self, parameters: "PulseWaveParameters", bpm=65, length=10, sampling_rate=90):
        self.bpm = bpm
        self.length = length
        self.sampling_rate = sampling_rate
        self.CUTOFF = 20
        self.STOP_ATTEN = 20

        self.hmm = HMM(time_steps=self.beats, parameters=parameters)

    def sample(self):
        state, parameters = self.hmm.sample()
        wave = [PulseModelRaw(**p) for s, p in zip(state, parameters)]

        indicator = [ArbitraryWaveform(waveform=s * np.ones_like(w.waveform)) for s, w in zip(state, wave)]
        shift = list(accumulate(map(len, wave[:-1])))

        deque(map(lambda xx, delta: xx.shift(delta), wave[1:], shift))
        deque(map(lambda xx, delta: xx.shift(delta), indicator[1:], shift))

        x = sum(wave).waveform
        t_raw = np.linspace(0, self.beats * self.beat_period, len(x))

        fx = interp1d(t_raw, x, kind="cubic")
        t_start = np.random.random() * (max(t_raw) - self.length)
        t = np.linspace(t_start, self.length + t_start, int(self.length * self.sampling_rate))

        x = fx(t)
        sos = cheby2(2, self.STOP_ATTEN, self.CUTOFF / (self.sampling_rate / 2), output="sos")
        x = sosfiltfilt(sos, x)

        y = sum(indicator).waveform
        fy = interp1d(t_raw, y, kind="cubic")
        y = fy(t) > 0.5

        t = t - min(t)
        return x, y, t
