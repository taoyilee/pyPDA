import os

from matplotlib import pyplot as plt
import logging
logger = logging.getLogger("pypda")

def plot_waveform(plot_dir, t, wave, x, y):
    plt.figure(figsize=(wave.beats, 6))
    plt.subplot(2, 1, 1)
    plt.title(f"Pulse Model")
    plt.ylabel("Blood Pressure (mmHg)")
    plt.xlabel("Time (Second)")
    plt.grid()
    plt.plot(t, x)
    plt.xlim([0, max(t)])
    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.ylabel("Abnormality")
    plt.yticks([0, 1])
    plt.xlim([0, max(t)])
    plt.tight_layout()
    output_plot = os.path.join(plot_dir, "sample_test.png")
    plt.savefig(output_plot)
    logger.debug(f"waveform plot saved to {output_plot}")
