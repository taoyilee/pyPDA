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
    plt.grid()
    plt.title(f"Pulse Model")
    plt.ylabel("Amplitude")
    plt.xlabel("Sample")
    plt.tight_layout()
    if png:
        plt.savefig(os.path.join(plot_dir, "pulse.png"))


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
