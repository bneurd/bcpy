from joblib import load
from sklearn.svm import SVC
from .Classifier import Classifier
from .training import register_training, Training
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


@register_training
class SVM(Training):

    def __init__(self, **kargs):
        self.clf = SVC(kernel="linear")

    def fit(self, X, y):
        self.clf.fit(X, y)
        return Classifier(self.clf)

    def load(self, filename):
        self.clf = load(filename)
        return Classifier(self.clf)


@register_training
class KNN(Training):

    def __init__(self, **kargs):
        self.clf = KNeighborsClassifier(**kargs)

    def fit(self, X, y):
        self.clf.fit(X, y)
        return Classifier(self.clf)

    def load(self, filename):
        self.clf = load(filename)
        return Classifier(self.clf)


@register_training
class LDA(Training):

    def __init__(self, **kargs):
        self.clf = LinearDiscriminantAnalysis(**kargs)

    def fit(self, X, y):
        self.clf.fit(X, y)
        return Classifier(self.clf)

    def load(self, filename):
        self.clf = load(filename)
        return Classifier(self.clf)
