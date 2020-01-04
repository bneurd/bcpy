import time
import threading
from .._handlers import properties
from abc import ABC, abstractmethod


class RealtimeError(Exception):
    pass


class Realtime(ABC):
    """Realtime abstract class
    """

    def __init__(self, options):
        self.channels = options["channels"]
        self.fs = options["fs"]

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send_data(self, eeg):
        pass


realtime_strategies = {}
qlock = threading.Lock()


def _visualize(acq, data, minimum_time=None):
    qlock.acquire()
    acq.show_realtime_data(data, minimum_time)
    qlock.release()


def register_realtime(cls):
    """ register a new strategy to realtime dictionary

    This function was made to be used as decorator on
    subclass of bcpy.realtimevisualization.Realtime

    Parameters
    ----------
    - cls : subclass of bcpy.realtimevisualization.Realtime
        subclass that will be register as an avaliable strategy

    Returns
    -------
    - subclass of bcpy.realtimevisualization.Realtime
        class passed on parameter

    Raises
    ------
    - RealtimeError
        raises when the class is already register on dictionary
    """

    if (cls.__name__ in realtime_strategies):
        raise RealtimeError(
            "Realtime strategy" + cls.__name__ +
            "already register in realtime_strategies")

    realtime_strategies[cls.__name__] = cls

    return cls


def realtimevisualization(r, dataIter, options):
    """Send data to GUI

    Parameters
    ----------
    - dataIter: `str` or `Realtime`
        Strategy to send data

    Returns
    -------
    - data: `generator` of `[n_channels]`
    """
    props = properties.Properties()
    if isinstance(r, str):
        if not (r in realtime_strategies):
            raise RealtimeError("Unknown realtime strategy {r}".format(r=r))

        # TODO: Sync this
        acq = realtime_strategies[r](options)
        time.sleep(0.5)
        acq.start()

        props.realtime_inst = acq
        intersec = options["intersection"] if "intersection" in options else 0

        data = next(dataIter)
        greater_diff = 1
        yield(data)
        threading.Thread(target=_visualize, args=(
            acq, data, True)).start()

        while True:
            data = next(dataIter)
            time_before_yield = time.time()
            yield(data)
            data_to_send = data[intersec:]
            diff = time.time() - time_before_yield
            greater_diff = diff if diff > greater_diff else greater_diff
            threading.Thread(target=_visualize, args=(
                acq, data_to_send)).start()
    elif isinstance(r, Realtime):
        acq = r

        props.realtime_inst = acq

        while True:
            data = next(dataIter)
            yield(data)
            threading.Thread(target=_visualize, args=(acq, data)).start()
