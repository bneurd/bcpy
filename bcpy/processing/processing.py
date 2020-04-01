import types
import numpy as np
from scipy import signal
from mne import set_eeg_reference
from abc import ABC, abstractmethod


class FilterError(Exception):
    pass


class Filter(ABC):
    """ Basic of all filter
    """
    @abstractmethod
    def process(self, data):
        """Process the filter and return the process data

        Parameters
        ----------
        data: `array like`
            frequency of transmission

        Returns
        -------
        filtered data : ndarray
        """
        return np.ndarray


class ButterBandPass(Filter):
    def __init__(self, lowcut, highcut, fs=256, order=4):
        nyq = fs * 0.5
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='bandpass')

        self.b = b
        self.a = a

    def process(self, data):
        return signal.filtfilt(self.b, self.a, data, axis=1)


class ButterLowPass(Filter):
    def __init__(self, lowcut, fs=256, order=4):
        nyq = fs * 0.5
        low = lowcut / nyq
        b, a = signal.butter(order, low, btype='lowpass')

        self.b = b
        self.a = a

    def process(self, data):
        return signal.filtfilt(self.b, self.a, data, axis=1)


class ButterHighPass(Filter):
    def __init__(self, highcut, fs=256, order=4):
        nyq = fs * 0.5
        high = highcut / nyq
        b, a = signal.butter(order, high, btype='highpass')

        self.b = b
        self.a = a

    def process(self, data):
        return signal.filtfilt(self.b, self.a, data, axis=1)


class Notch(Filter):
    def __init__(self, cutoff, var=1, fs=256, order=4):
        nyq = fs * 0.5
        low = (cutoff - var) / nyq
        high = (cutoff + var) / nyq

        b, a = signal.iirfilter(
            order, [low, high], btype='bandstop', ftype="butter")

        self.b = b
        self.a = a

    def process(self, data):
        return signal.sfiltfilt(self.b, self.a, data, axis=-1)


def bandfilter(bufferGen: types.GeneratorType,
               lo: float = None,
               hi: float = None) -> types.GeneratorType:
    """ apply a butterworth filter to de data

    Parameters
    ----------
    bufferGen: `generator` of buffers
        Generator of the buffers to apply the filter
    lo: float
        When **lo** is specified, all frequencies under **lo** will be filtered
    hi: float
        when **hi** is specified, all frequencies above **hi** will be filtered
    fs: int, optional
        Sample frequency of the signal (default to 256)
    order: int, optional
        Filter order (default to 4)

    Yield
    -----
    filterd buffer: array
        array with the same buffer, but filtered

    Raises
    ------
    ValueError
        When none of the **hi** and **lo** are specify
    """

    while True:
        raw = next(bufferGen)
        raw.filter(l_freq=lo, h_freq=hi, verbose=False)
        yield raw


def notch(bufferGen: types.GeneratorType,
          freqs: list(),
          **kargs) -> types.GeneratorType:
    """ Apply notch filter

    Parameters
    ----------
    bufferGen: `generator` of objects
        Generator of the buffers to apply the filter
    freqs: `float` | `list` of `float`
        frequency to apply the notch filter

    Yield
    -----
    filterd buffer: object
        object with notch applied

    """
    while(True):
        raw = next(bufferGen)
        raw.notch_filter(freqs, **kargs)
        yield raw


def car(bufferGen, **kargs):
    while True:
        raw = next(bufferGen)
        inst, data = set_eeg_reference(raw, verbose=False, **kargs)
        yield inst


def drop_channels(bufferGen, channels):
    while True:
        raw = next(bufferGen)
        raw.drop_channels(channels)
        yield raw
