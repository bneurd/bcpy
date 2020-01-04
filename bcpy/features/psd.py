import numpy as np
from scipy import signal


def psd(signal_generator, fs=256, nperseg=None, noverlap=None, average=False, **kargs):
    while True:
        signal_buff = next(signal_generator)
        signal_buff = np.array(signal_buff).T
        psds = []
        for channel in signal_buff:
            f, psd_signal = signal.welch(channel,
                                         fs=fs,
                                         nperseg=nperseg,
                                         noverlap=noverlap,
                                         **kargs)
            psds.append(psd_signal)
        if average:
            yield (f, np.average(np.array(psds), axis=0))
        else:
            yield (f, np.array(psds))


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
