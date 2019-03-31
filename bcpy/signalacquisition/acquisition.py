from abc import ABC, abstractmethod
from bcpy.serve.flask import start_server


class AcquisitionError(Exception):
    pass


class Acquisition(ABC):
    """
    """

    def __init__(self):
        self.server_thread = start_server()

    @abstractmethod
    def get_data(self):
        return self, AcquisitionData()

    @abstractmethod
    def terminate(self):
        pass


class AcquisitionData():
    def __init__(self):
        self.marker = -1
        # eeg timestamp, eeg data channels, markers
        self.data = [[], [], []]

    def add_data(self, timestamp, eeg):
        self.data[0].append(timestamp)
        self.data[1].append(eeg)
        self.data[2].append(self.marker)
        # print(self.marker)

    def set_marker(self, marker):
        self.marker = marker

    def get_values(self):
        return self.data


acquisition_strategies = {}


def register_acquisition(cls):
    """ register a new strategy to acquisition dictionary

    This function was made to be used as decorator on 
    subclass of bcpy.acquisition.Acquisition

    Parameters
    ----------
    - cls : subclass of bcpy.acquisition.Acquisition
        subclass that will be register as an avaliable strategy

    Returns
    -------
    - subclass of bcpy.acquisition.Acquisition
        class passed on parameter

    Raises
    ------
    - AcquisitionError
        raises when the class is already register on dictionary
    """

    if (cls.__name__ in acquisition_strategies):
        raise AcquisitionError(
            "Acquisition strategy" + cls.__name__ +
            "already register in acquisition_strategies")

    acquisition_strategies[cls.__name__] = cls

    return cls


def getdata(a, *args, **kargs):
    if isinstance(a, str):
        if not (a in acquisition_strategies):
            raise AcquisitionError("Unknown acquisition {a}".format(a=a))

        acq = acquisition_strategies[a](**kargs)
        return acq.get_data(*args)
    elif isinstance(a, Acquisition):
        return a.get_data(*args)
