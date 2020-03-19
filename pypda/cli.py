"""Console script for pypda."""
import logging
import sys

import click

logger = logging.getLogger("pypda")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
DEBUG = False


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    global DEBUG
    DEBUG = debug
    if DEBUG:
        console_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    logger.info('Debug mode is %s' % ('on' if debug else 'off'))


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
    from pypda.api import sample

    return sample(plot_dir=plot_dir, length=length, bpm=bpm, sampling_rate=sampling_rate, png=png)


@cli.command()  # @cli, not @click!
@click.option('--plot-dir', default='plot', help='Plot output directory')
@click.option('--length', default=10, help='Length of the sample in seconds')
@click.option('--bpm', default=65, help='BPM')
@click.option('--sampling-rate', default=90, help='Sampling rate Hz')
@click.option('--png/--no-png', default=False)
def sample_test(plot_dir='plot', length=10, bpm=65, sampling_rate=90, png=False):
    from pypda.api import sample_test

    return sample_test(plot_dir=plot_dir, length=length, bpm=bpm, sampling_rate=sampling_rate, png=png)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
