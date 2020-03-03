"""Console script for pypda."""
import sys

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
    from pypda.pulse_wave import PulseWave
    import os
    os.makedirs(plot_dir, exist_ok=True)
    import matplotlib.pyplot as plt
    from pypda.parameters import PulseWaveParameters
    p = PulseWaveParameters()

    p.normal.beat_length.mean = 100
    p.abnormal.diastolic_baseline.mean = 90
    p.abnormal.diastolic_baseline.scale = 20
    p.abnormal.beat_length.mean = 0.6 * p.normal.beat_length.mean
    p.abnormal.pulse_amplitudes[1].mean = 3.5
    p.abnormal.pulse_amplitudes[2].mean = 4.5
    p.abnormal.pulse_amplitudes[3].mean = 2.2
    p.abnormal.pulse_amplitudes[4].mean = 1.1
    p.normal.scale = (
        10, 5, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2)

    p.abnormal.scale = (10, 20, .2, .2, .2, .2, .2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    print(f"Parameters for normal =\n{p.normal}")
    print(f"Parameters for abnormal =\n{p.abnormal}")
    wave = PulseWave(parameters=p, bpm=bpm, length=length, sampling_rate=sampling_rate)
    x, y, t = wave.sample()

    plt.figure(figsize=(wave.beats, 6))
    plt.subplot(2, 1, 1)
    plt.title(f"Pulse Model")
    plt.ylabel("Blood Pressure (mmHg)")
    plt.xlabel("Time (Second)")
    plt.grid()
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


@cli.command()  # @cli, not @click!
@click.option('--plot-dir', default='plot', help='Plot output directory')
@click.option('--length', default=10, help='Length of the sample in seconds')
@click.option('--bpm', default=65, help='BPM')
@click.option('--sampling-rate', default=90, help='Sampling rate Hz')
@click.option('--png/--no-png', default=False)
def sample_test(plot_dir='plot', length=10, bpm=65, sampling_rate=90, png=False):
    """

    :param plot_dir:
    :param length: in seconds
    :param sampling_rate: in Hz
    :param png:
    :return:
    """
    from pypda.pulse_wave import PulseWave
    import os
    os.makedirs(plot_dir, exist_ok=True)
    import matplotlib.pyplot as plt
    from pypda.parameters import PulseWaveParameters
    p = PulseWaveParameters()

    p.normal.beat_length.mean = 100
    p.abnormal.diastolic_baseline.mean = 86
    p.abnormal.diastolic_baseline.scale = 13
    p.abnormal.beat_length.mean = 0.3 * p.normal.beat_length.mean
    p.abnormal.pulse_amplitudes[1].mean = 3.1
    p.abnormal.pulse_amplitudes[2].mean = 4.1
    p.abnormal.pulse_amplitudes[3].mean = 2.1
    p.abnormal.pulse_amplitudes[4].mean = 0.9
    p.abnormal.delta_time[0].mean = 6
    p.abnormal.delta_time[1].mean = 7
    p.abnormal.delta_time[2].mean = 5
    p.abnormal.delta_time[3].mean = 7.3
    p.normal.scale = (
        10, 5, .2, .2, .2, .2, .2, .2, .2, .2, .2, .5, .5, .5, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2, .2)

    p.abnormal.scale = (10, 20, .2, .2, .2, .2, .2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    print(f"Parameters for normal =\n{p.normal}")
    print(f"Parameters for abnormal =\n{p.abnormal}")
    wave = PulseWave(parameters=p, bpm=bpm, length=length, sampling_rate=sampling_rate)
    x, y, t = wave.sample()

    plt.figure(figsize=(wave.beats, 6))
    plt.subplot(2, 1, 1)
    plt.title(f"Pulse Model")
    plt.ylabel("Blood Pressure (mmHg)")
    plt.xlabel("Time (Second)")
    plt.grid()
    plt.plot(t, x)
    plt.xlim([0, length])
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.ylabel("Abnormality")
    plt.yticks([0, 1])
    plt.xlim([0, length])
    plt.tight_layout()
    if png:
        plt.savefig(os.path.join(plot_dir, "sample_test.png"))
    return x, y, t


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
