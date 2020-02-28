"""Console script for pypda."""
import sys
from itertools import accumulate

import click

DEBUG = False


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    global DEBUG
    DEBUG = debug
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()  # @cli, not @click!
@click.option('--plot-dir', default='plot', help='Plot output directory')
@click.option('--png/--no-png', default=False)
def wavelet(plot_dir='plot', png=False):
    import os
    os.makedirs(plot_dir, exist_ok=True)
    from pypda.wavelets import TriangGaussian
    import matplotlib.pyplot as plt
    w = TriangGaussian()
    w.shift(10)
    plt.plot(w.waveform)
    plt.grid()
    plt.title(f"Smoothed Triangular Window m_triangle={w.triang_m}, m_gaussian={w.gaussian_m} std={w.gaussian_std}")
    plt.ylabel("Amplitude")
    plt.xlabel("Sample")
    plt.tight_layout()
    if png:
        plt.savefig(os.path.join(plot_dir, "triangle.png"))


@cli.command()  # @cli, not @click!
@click.option('--plot-dir', default='plot', help='Plot output directory')
@click.option('--png/--no-png', default=False)
def pulse(plot_dir='plot', png=False):
    import os
    os.makedirs(plot_dir, exist_ok=True)
    from pypda.pulse_model import PulseModelRaw
    import matplotlib.pyplot as plt
    w = PulseModelRaw()
    plt.plot(w.waveform)
    for i, wavelet in enumerate(w.wavelets):
        plt.plot(wavelet.waveform, linestyle="--", label=f"component {i + 1}")
    plt.grid()
    plt.title(f"Pulse Model")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.xlabel("Sample")
    plt.tight_layout()
    if png:
        plt.savefig(os.path.join(plot_dir, "pulse.png"))


@cli.command()  # @cli, not @click!
@click.option('--plot-dir', default='plot', help='Plot output directory')
@click.option('--length', default=10, help='Length of the sample in seconds')
@click.option('--bpm', default=65, help='BPM')
@click.option('--sampling-rate', default=90, help='Sampling rate Hz')
@click.option('--png/--no-png', default=False)
def sample(plot_dir='plot', length=10, bpm=65, sampling_rate=90, png=False):
    """

    :param plot_dir:
    :param length: in seconds
    :param sampling_rate: in Hz
    :param png:
    :return:
    """
    import os
    from pypda.hmm import HMM
    from scipy.interpolate import interp1d
    from scipy.signal import cheby2, sosfiltfilt
    os.makedirs(plot_dir, exist_ok=True)
    from pypda.pulse_model import PulseModelRaw
    from pypda.wavelets import ArbitraryWaveform
    import matplotlib.pyplot as plt
    from collections import deque
    import numpy as np

    CUTOFF = 20
    STOP_ATTEN = 20

    beats = np.ceil(bpm * length / 60).astype(int) + 1
    raw_beat_length = 100
    beat_period = 1 / (bpm / 60)  # in seconds

    hmm = HMM(time_steps=beats,
              normal_mean=(raw_beat_length, 80, 8, 3, 4, 2, 1,
                           15, 10, 10, 10, 20, 20, 20, 20, 20, 16, 16, 16, 16, 16, 2, 2, 2, 2, 2),
              normal_scale=(10, 5, .2, .2, .2, .2, .2, .2,
                            .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2),
              abnormal_mean=(0.6 * raw_beat_length, 90, 8, 3.5, 4.5, 2.2,
                             1.1, 10, 10, 10, 10, 20, 20, 20, 20, 20, 16, 16, 16, 16, 16,
                             2, 2, 2, 2, 2),
              abnormal_scale=(10, 20, .2, .2, .2, .2, .2,
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
    state, parameters = hmm.sample()
    wave = [PulseModelRaw(**p) for s, p in zip(state, parameters)]
    for s, w in zip(state, wave):
        print("ABNORMAL" if s else "NORMAL", w.samples)
    indicator = [ArbitraryWaveform(waveform=s * np.ones_like(w.waveform)) for s, w in zip(state, wave)]
    shift = list(accumulate(map(len, wave[:-1])))

    deque(map(lambda xx, delta: xx.shift(delta), wave[1:], shift))
    deque(map(lambda xx, delta: xx.shift(delta), indicator[1:], shift))

    plt.figure(figsize=(beats, 6))
    plt.subplot(2, 1, 1)
    plt.title(f"Pulse Model")
    plt.ylabel("Blood Pressure (mmHg)")
    plt.xlabel("Time (Second)")
    plt.grid()
    x = sum(wave).waveform
    t_raw = np.linspace(0, beats * beat_period, len(x))

    fx = interp1d(t_raw, x, kind="cubic")
    t_start = np.random.random() * (max(t_raw) - length)
    t = np.linspace(t_start, length + t_start, length * sampling_rate)

    x = fx(t)
    sos = cheby2(2, STOP_ATTEN, CUTOFF / (sampling_rate / 2), output="sos")
    x = sosfiltfilt(sos, x)

    y = sum(indicator).waveform
    fy = interp1d(t_raw, y, kind="cubic")
    y = fy(t) > 0.5

    t = t - min(t)

    plt.plot(t, x)
    plt.xlim([0, length])
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.ylabel("Abnormality")
    plt.yticks([0, 1])
    plt.xlim([0, length])
    plt.tight_layout()
    if png:
        plt.savefig(os.path.join(plot_dir, "sample.png"))
    return x, y, t


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
