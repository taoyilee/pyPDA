import numpy as np


class ParameterMeanScale:
    def __init__(self, mean=0.0, scale=1.0):
        self.mean = mean
        self.scale = scale


class PulseParameters:
    def __init__(self, beat_length=100,
                 diastolic_baseline=80,
                 pulse_amplitudes=(8, 3, 4, 2, 1),
                 delta_time=(10, 10, 10, 10),
                 triangle_m=(20, 20, 20, 20, 20),
                 gaussian_m=(16, 16, 16, 16, 16),
                 gaussian_std=(2, 2, 2, 2, 2)):
        self.beat_length = ParameterMeanScale(beat_length, 10)
        self.diastolic_baseline = ParameterMeanScale(diastolic_baseline, 5)
        self.pulse_amplitudes = [ParameterMeanScale(p, 0.2) for p in pulse_amplitudes]
        self.delta_time = [ParameterMeanScale(p, 0.2) for p in delta_time]
        self.triangle_m = [ParameterMeanScale(p, 0.2) for p in triangle_m]
        self.gaussian_m = [ParameterMeanScale(p, 0.2) for p in gaussian_m]
        self.gaussian_std = [ParameterMeanScale(p, 0.2) for p in gaussian_std]

    def __len__(self):
        return len(self.features)

    @property
    def features(self):
        _features = [self.beat_length, self.diastolic_baseline]
        _features.extend(self.pulse_amplitudes)
        _features.extend(self.delta_time)
        _features.extend(self.triangle_m)
        _features.extend(self.gaussian_m)
        _features.extend(self.gaussian_std)

        return _features

    @property
    def scale(self) -> np.ndarray:
        return np.array(list(map(lambda x: getattr(x, "scale"), self.features)))

    @scale.setter
    def scale(self, value):
        assert len(value) == len(self), f"{value} must have length = {self.__len__()}"
        for i, v in enumerate(value):
            self.features[i].scale = v

    @property
    def mean(self) -> np.ndarray:
        return np.array(list(map(lambda x: getattr(x, "mean"), self.features)))

    @mean.setter
    def mean(self, value):
        assert len(value) == len(self), f"{value} must have length = {self.__len__()}"
        for i, v in enumerate(value):
            self.features[i].mean = v

    @property
    def feature_names(self):
        _feature_names = ["beat_length", "diastolic_baseline"]

        _feature_names.extend([f"pulse_amplitudes[{i}]" for i in range(len(self.pulse_amplitudes))])
        _feature_names.extend([f"delta_time[{i}]" for i in range(len(self.delta_time))])
        _feature_names.extend([f"triangle_m[{i}]" for i in range(len(self.triangle_m))])
        _feature_names.extend([f"gaussian_m[{i}]" for i in range(len(self.gaussian_m))])
        _feature_names.extend([f"gaussian_std[{i}]" for i in range(len(self.gaussian_std))])
        return _feature_names

    def __repr__(self):
        _repr = ""
        for k, v in zip(self.feature_names, self.features):
            _repr += f"{k}: {v.mean}+/-{v.scale}\n"
        return _repr


class PulseWaveParameters:
    def __init__(self, normal: "PulseParameters" = PulseParameters(),
                 abnormal: "PulseParameters" = PulseParameters()):
        self.normal = normal
        self.abnormal = abnormal

        assert len(self.normal) == len(self.abnormal), \
            f"#parameters for normal={len(self.normal)} must be equal to #parameters for abnormal={len(self.abnormal)}"
