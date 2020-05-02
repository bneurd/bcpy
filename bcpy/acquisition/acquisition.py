from abc import ABC, abstractmethod


class AcquisitionError(Exception):
    pass


class Acquisition(ABC):
    """Acquisition abstract class
    """

    @abstractmethod
    def get_data(self):
        return iter()

    @abstractmethod
    def get_label(self):
        return iter()


acquisition_strategies = {}


def register_acquisition(cls):
    """ register a new strategy to acquisition dictionary

    This function was made to be used as decorator on
    subclass of bcpy.acquisition.Acquisition

    Parameters
    ----------
    cls : subclass of bcpy.acquisition.Acquisition
        subclass that will be register as an avaliable strategy

    Returns
    -------
    subclass of bcpy.acquisition.Acquisition
        class passed on parameter

    Raises
    ------
    AcquisitionError
        raises when the class is already register on dictionary
    """

    if (cls.__name__ in acquisition_strategies):
        raise AcquisitionError(
            "Acquisition strategy" + cls.__name__ +
            "already register in acquisition_strategies")

    acquisition_strategies[cls.__name__] = cls

    return cls


def getdata(strategy, *args, **kargs):
    """Get data using some strategy

    Parameters
    ----------
    strategy: str or Acquisition
        Strategy to get data
    *args:
        Strategy's get_data paramns
    **kargs:
        Strategy's instance paramns

    Yield
    -------
    data: :obj:`list` of n_channels
        Data for all channels on one interation
    """

    if isinstance(strategy, str):
        if not (strategy in acquisition_strategies):
            raise AcquisitionError(
                "Unknown acquisition {a}".format(a=strategy))

        acq = acquisition_strategies[strategy](**kargs)
        # acq.get_data(*args)
        return acq.get_data(*args)
    elif isinstance(strategy, Acquisition):
        return strategy.get_data(*args)


def getdata_label(strategy, *args, **kargs):
    """Get data using some strategy

    Parameters
    ----------
    strategy: str or Acquisition
        Strategy to get data
    *args:
        Strategy's get_data paramns
    **kargs:
        Strategy's instance paramns

    Yield
    -------
    data: :obj:`list` of n_channels
        Data for all channels on one interation
    """

    if isinstance(strategy, str):
        if not (strategy in acquisition_strategies):
            raise AcquisitionError(
                "Unknown acquisition {a}".format(a=strategy))

        acq = acquisition_strategies[strategy](**kargs)
        # acq.get_data(*args)
        return acq.get_data(*args), acq.get_label(*args)
    elif isinstance(strategy, Acquisition):
        return strategy.get_data(*args), strategy.get_label(*args)
