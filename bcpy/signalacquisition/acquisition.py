from abc import ABC, abstractmethod


class AcquisitionError(Exception):
    pass


class Acquisition(ABC):
    """
    """
    @abstractmethod
    def get_data(self):
        return iter()

    @abstractmethod
    def terminate(self):
        pass


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
        # acq.get_data(*args)
        return acq.get_data()
    elif isinstance(a, Acquisition):
        return a.get_data(*args)
