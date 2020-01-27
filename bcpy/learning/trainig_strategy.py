from sklearn.svm import SVC
from joblib import load
from .Classifier import Classifier
from .training import register_training, Training


@register_training
class SVM(Training):
    """Reciver using the protocol LSL to get data

    Parameters
    ----------
    frequency: `int`
        frequency of transmission
    channels: :obj:`list` of `str`
        list of eletrodos utilized on the experiment
    """

    def __init__(self, **kargs):
        print(kargs)
        self.clf = SVC(**kargs)

    def fit(self, X, y):
        self.clf.fit(X, y)
        return Classifier(self.clf)

    def load(self, filename):
        self.clf = load(filename)
        return Classifier(self.clf)
