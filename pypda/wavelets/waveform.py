import abc

import numpy as np


class Waveform(abc.ABC):
    _waveform = None

    @property
    @abc.abstractmethod
    def waveform(self) -> np.ndarray:
        raise NotImplementedError

    def __len__(self):
        return len(self.waveform)

    def shift(self, shift=0):
        """

        :param shift: shift > 0 means shifting right. e.g., shift = 3: [1 2 3 4] => [0 0 0 1 2 3 4]
        :return:
        """
        assert isinstance(self.waveform, np.ndarray)
        if shift > 0:
            self._waveform = np.concatenate((np.zeros(shift), self._waveform))
        if shift < 0:
            self._waveform = np.concatenate((self._waveform, np.zeros(shift)))

    def __add__(self, other: "Waveform"):
        assert isinstance(other, Waveform), f"{other} is not a Waveform"
        w = ArbitraryWaveform(length=max(len(self), len(other)))
        w.waveform[:len(self)] = self.waveform
        w.waveform[:len(other)] += other.waveform
        return w

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)


class ArbitraryWaveform(Waveform):
    def __init__(self, length=10, waveform=None):
        if waveform is not None:
            assert waveform.ndim == 1
            self._waveform = waveform
        else:
            self._waveform = np.zeros(length)

    @property
    def waveform(self) -> np.ndarray:
        return self._waveform

    @waveform.setter
    def waveform(self, value):
        self._waveform[:len(value)] = value
