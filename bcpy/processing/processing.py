import types
import numpy as np
from scipy import signal
from sklearn.preprocessing import StandardScaler
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
               hi: float = None,
               fs: int = 256,
               order: int = 4) -> types.GeneratorType:
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

    if lo and hi:
        while(True):
            buff = np.array(next(bufferGen)).T
            yield(ButterBandPass(lo, hi, fs=256, order=4).process(buff).T)

    elif lo:
        while(True):
            buff = np.array(next(bufferGen)).T
            yield(ButterHighPass(lo, fs=256, order=4).process(buff).T)

    elif hi:
        while(True):
            buff = np.array(next(bufferGen)).T
            yield(ButterLowPass(hi, fs=256, order=4).process(buff).T)

    raise ValueError("at least one of hi and lo must be specified")


def notch(bufferGen: types.GeneratorType,
          cutoff: float,
          var: float = 1,
          fs: int = 256,
          order: int = 4) -> types.GeneratorType:
    """ Apply notch filter

    Parameters
    ----------
    bufferGen: `generator` of buffers
        Generator of the buffers to apply the filter
    cutoff: float
        frequency to apply the notch filter
    var: float, option
        frequency variance
        this will tell what is the exact interval to apply the notch filter

        **var=0.5 -> will apply the filter between cutoff-0.5 and cutoff+0.5**

        **var=1 -> will apply the filter between cutoff-1 and cutoff+1**

        ...

        **var=n -> will apply the filter between cutoff-n and cutoff+n**

        (default to 1)
    fs: int, optional
        Sample frequency of the signal (default to 256)
    order: int, optional
        Filter order (default to 4)

    Yield
    -----
    filterd buffer: array
        array with the same buffer, but filtered

    """
    while(True):
        buff = np.array(next(bufferGen)).T
        yield(Notch(cutoff, var=1, fs=256, order=4).process(buff).T)


def standard_scaller(featureGen: types.GeneratorType):
    ss = StandardScaler()
    while True:
        feature = next(featureGen)
        if (len(feature) > 1):
            yield feature[0], ss.fit_transform(feature[1])
        else:
            yield ss.fit_transform(feature)
