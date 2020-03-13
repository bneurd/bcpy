import numpy as np
from mne.time_frequency import psd_multitaper


def psd(generator,
        **kargs):
    while True:
        raw = next(generator)
        raw.plot_psd(fmax=30)
        psd, freqs = psd_multitaper(raw, fmax=30)
        yield (freqs, psd)


def band_extract(frequencies, psd, fmin, fmax):
    if len(psd.shape) == 2:
        pass
    first_index = None
    last_index = None
    for f_idx in range(len(frequencies)):
        if not first_index and frequencies[f_idx] >= fmin:
            first_index = f_idx
        if frequencies[f_idx] > fmax:
            last_index = f_idx
            break
    band = psd[first_index:last_index]
    return np.average(band)
