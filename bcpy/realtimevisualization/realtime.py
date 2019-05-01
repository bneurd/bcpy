from abc import ABC, abstractmethod
import time


class RealtimeError(Exception):
    pass


class Realtime(ABC):
    """
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
    if isinstance(r, str):
        if not (r in realtime_strategies):
            raise RealtimeError("Unknown realtime strategy {r}".format(r=r))

        # TODO: Sync this
        acq = realtime_strategies[r](options)
        time.sleep(0.5)
        acq.start()
        return acq.show_realtime_data(dataIter)
    elif isinstance(r, Realtime):
        r.start()
        return r.show_realtime_data(dataIter)
