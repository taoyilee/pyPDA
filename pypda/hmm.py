import random
from itertools import product
from typing import Union, Iterable

import numpy as np


class CPT:
    def __init__(self, n_variables=3, states=2, definition="P(A|B,C)"):
        self.n = n_variables
        self.k = states
        self.definition = definition
        cpt_init_data = np.random.rand(states ** n_variables)
        self._cpt = {}
        for i, row in enumerate(product(range(self.k), repeat=self.n)):
            self._cpt[row] = cpt_init_data[i]

    def __getitem__(self, item):
        return self._cpt[item]

    def __setitem__(self, key, value):
        self._cpt[key] = value

    def sample_conditioned(self, *conditions: Union[Iterable, int]) -> int:
        try:
            sample_weights = [self._cpt[tuple([ki] + list(int(c) for c in conditions))] for ki in range(self.k)]
        except TypeError:  # conditions not iterable
            sample_weights = [self._cpt[ki, conditions] for ki in range(self.k)]
        return int(random.choices(range(self.k), weights=sample_weights)[0])


class HMM:
    def __init__(self, time_steps=100,
                 normal_mean=(1, 2, 3, 4, 5), normal_scale=(1, 1, 1, 1, 1),
                 abnormal_mean=(2, 4, 6, 8, 10), abnormal_scale=(1, 2, 3, 4, 5)):
        self.SEVERITY_STEPS = 3
        self.prior_normal = 0.99
        self.output_features = len(normal_mean)
        self.normal_mean = normal_mean
        assert len(normal_scale) == self.output_features, \
            f"len(normal_scale)={len(normal_scale)} must be equal to #output_features={self.output_features}"
        self.normal_scale = normal_scale
        assert len(abnormal_mean) == self.output_features, \
            f"len(abnormal_mean)={len(abnormal_mean)} must be equal to #output_features={self.output_features}"
        self.abnormal_mean = abnormal_mean
        assert len(abnormal_scale) == self.output_features, \
            f"len(abnormal_scale)={len(abnormal_scale)} must be equal to #output_features={self.output_features}"
        self.abnormal_scale = abnormal_scale

        self.T = time_steps
        self.cpt_n_transistion = CPT(n_variables=3, states=2, definition="P(n_{t+1}|n_{t}, s_{t-1}")

        self.cpt_n_transistion[0, 0, 0] = 0.99
        self.cpt_n_transistion[1, 0, 0] = 0.01
        self.cpt_n_transistion[0, 0, 1] = 0.85
        self.cpt_n_transistion[1, 0, 1] = 0.15
        self.cpt_n_transistion[0, 0, 2] = 0.8
        self.cpt_n_transistion[1, 0, 2] = 0.2

        self.cpt_n_transistion[0, 1, 0] = 0.3
        self.cpt_n_transistion[1, 1, 0] = 0.7
        self.cpt_n_transistion[0, 1, 1] = 0.6
        self.cpt_n_transistion[1, 1, 1] = 0.4
        self.cpt_n_transistion[0, 1, 2] = 0.4
        self.cpt_n_transistion[1, 1, 2] = 0.6

        self.cpt_n_s_emission = CPT(n_variables=2, states=self.SEVERITY_STEPS, definition="P(s_{t}|n_{t}")
        self.cpt_n_s_emission[0, 0] = 0.6
        self.cpt_n_s_emission[1, 0] = 0.2
        self.cpt_n_s_emission[2, 0] = 0.1

        self.cpt_n_s_emission[0, 1] = 0.5
        self.cpt_n_s_emission[1, 1] = 0.3
        self.cpt_n_s_emission[2, 1] = 0.15

    def sample(self):
        from sklearn.datasets import make_gaussian_quantiles
        features_n, severity_n = make_gaussian_quantiles(mean=None, cov=1.0, n_samples=10 * self.T,
                                                         n_features=self.output_features, n_classes=self.SEVERITY_STEPS,
                                                         shuffle=True, random_state=None)
        features_n = [features_n[severity_n == s, :] for s in range(self.SEVERITY_STEPS)]
        features_a, severity_a = make_gaussian_quantiles(mean=None, cov=1.0, n_samples=10 * self.T,
                                                         n_features=self.output_features, n_classes=self.SEVERITY_STEPS,
                                                         shuffle=True, random_state=None)
        features_a = [features_a[severity_a == s, :] for s in range(self.SEVERITY_STEPS)]
        x = np.zeros(self.T).astype(int)
        s = np.zeros(self.T).astype(int)
        y = [{} for _ in range(self.T)]
        for i in range(self.T):
            if i == 0:
                x[0] = random.choices([0, 1], weights=[self.prior_normal, 1 - self.prior_normal])[0]
            else:
                x[i] = self.cpt_n_transistion.sample_conditioned(x[i - 1], s[i - 1])
            s[i] = self.cpt_n_s_emission.sample_conditioned(x[i])

            if x[i]:  # abnormal
                _idx = np.random.choice(range(features_a[s[i]].shape[0]))
                features = features_a[s[i]][_idx, :] * self.abnormal_scale + self.abnormal_mean
            else:  # normal
                _idx = np.random.choice(range(features_n[s[i]].shape[0]))
                features = features_a[s[i]][_idx, :] * self.normal_scale + self.normal_mean
            y[i]['samples'] = int(features[0])
            y[i]['baseline'] = features[1]

            y[i]['pulse_amplitudes'] = features[2:7]
            y[i]['delta_time'] = features[7:11].astype(int)
            y[i]['triangle_m'] = features[11:16].astype(int)
            y[i]['gaussian_m'] = features[16:21].astype(int)
            y[i]['gaussian_std'] = features[21:26]
        return x, y
