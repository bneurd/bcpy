from abc import ABC, abstractmethod
from scipy import signal
import numpy as np


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
        - data: `array like`
            frequency of transmission

        Returns
        -------
        - array
            process data
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


def apply_filter(dataIter, lo=None, hi=None, **kargs):
    if lo and hi:
        while(True):
            buff = np.array(next(dataIter)).T
            yield(ButterBandPass(lo, hi, **kargs).process(buff).T)
    elif lo:
        while(True):
            buff = np.array(next(dataIter)).T
            yield(ButterLowPass(lo, **kargs).process(buff).T)
    elif hi:
        while(True):
            buff = np.array(next(dataIter)).T
            yield(ButterHighPass(hi, **kargs).process(buff).T)


def notch(dataIter, cutoff, **kargs):
    while(True):
        buff = np.array(next(dataIter)).T
        yield(Notch(cutoff, **kargs).process(buff).T)
