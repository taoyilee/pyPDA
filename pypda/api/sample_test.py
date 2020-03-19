import logging
logger = logging.getLogger("pypda")

from pypda.api import plot_waveform


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
    logger.debug(f"Parameters for normal =\n{p.normal}")
    logger.debug(f"Parameters for abnormal =\n{p.abnormal}")
    wave = PulseWave(parameters=p, bpm=bpm, length=length, sampling_rate=sampling_rate)
    x, y, t = wave.sample()
    if png:
        plot_waveform(plot_dir, t, wave, x, y)
    return x, y, t


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
    logger.debug(f"Parameters for normal =\n{p.normal}")
    logger.debug(f"Parameters for abnormal =\n{p.abnormal}")
    wave = PulseWave(parameters=p, bpm=bpm, length=length, sampling_rate=sampling_rate)
    x, y, t = wave.sample()
    if png:
        plot_waveform(plot_dir, t, wave, x, y)
    return x, y, t
