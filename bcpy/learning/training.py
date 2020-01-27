import numpy as np
from abc import ABC, abstractmethod
from .._handlers import stop_execution, properties
from .Classifier import Classifier

props = properties.Properties()


class TrainingError(Exception):
    pass


class Training(ABC):
    """Training abstract class
    """

    @abstractmethod
    def fit(self, X, y) -> Classifier:
        pass

    @abstractmethod
    def load(self, filename) -> Classifier:
        pass


training_strategies = {}


def register_training(cls):
    """ register a new strategy to training dictionary

    This function was made to be used as decorator on
    subclass of bcpy.training.training

    Parameters
    ----------
    cls : subclass of bcpy.training.training
        subclass that will be register as an avaliable strategy

    Returns
    -------
    subclass of bcpy.training.training
        class passed on parameter

    Raises
    ------
    trainingError
        raises when the class is already register on dictionary
    """

    if (cls.__name__ in training_strategies):
        raise TrainingError(
            "training strategy" + cls.__name__ +
            "already register in training_strategies")

    training_strategies[cls.__name__] = cls

    return cls


def training(strategy, X_gen, y_gen,
             n_of_iterations: int = None,
             verbose=False,
             options={}):
    """Get data using some strategy

    Parameters
    ----------
    strategy: str or Training
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
    acq = None
    if isinstance(strategy, str):
        if not (strategy in training_strategies):
            raise TrainingError(
                "Unknown Training {a}".format(a=strategy))

        acq = training_strategies[strategy](**options)
    elif isinstance(strategy, Training):
        acq = strategy
    else:
        raise TrainingError(
            "Unknown Training {a}".format(a=strategy))
    iterations = 0
    stop_execution.handle_stop_signal()
    X = []
    y = []
    while props.running:
        if n_of_iterations is not None and iterations >= n_of_iterations:
            break
        try:
            data = next(X_gen)
            label = next(y_gen)
        except Exception:
            break
        if (len(data) > 1):
            X.append(data[1])
        else:
            X.append(data)
        y.append(label)
        iterations += 1
    X = np.array(X)
    X = X.reshape(X.shape[0], -1)
    y = np.array(y)
    if verbose:
        print(f'X shape: {X.shape}, y shape: {y.shape}')
    return acq.fit(X, y)


def load_training(strategy, filename, **kargs) -> Classifier:
    acq: Training = None
    if isinstance(strategy, str):
        if not (strategy in training_strategies):
            raise TrainingError(
                "Unknown Training {a}".format(a=strategy))

        acq: Training = training_strategies[strategy](**kargs)
    elif isinstance(strategy, Training):
        acq: Training = strategy
    else:
        raise TrainingError(
            "Unknown Training {a}".format(a=strategy))
    return acq.load(filename)
