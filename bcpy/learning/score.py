import numpy as np
from .._handlers import stop_execution, properties
from .Classifier import Classifier

props = properties.Properties()


def score(classifier: Classifier, X_gen, y_gen,
          n_of_iterations: int = None,
          verbose=False,
          **kargs):
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
    clf = classifier.clf
    return clf.score(X, y)
