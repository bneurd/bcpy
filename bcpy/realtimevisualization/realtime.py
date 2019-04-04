from abc import ABC, abstractmethod


class RealtimeError(Exception):
    pass


class Realtime(ABC):
    """
    """

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
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


def realtimevisualization(r):
    if isinstance(r, str):
        if not (r in realtime_strategies):
            raise RealtimeError("Unknown realtime strategy {r}".format(r=r))

        acq = realtime_strategies[r]()
        return acq
    elif isinstance(r, Realtime):
        return r
