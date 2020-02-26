from joblib import load
from sklearn.svm import SVC, SVR
from .Classifier import Classifier, OneVsAllClassifier
from .training import register_training, Training
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_selection import RFE


@register_training
class SVM(Training):

    def __init__(self, **kargs):
        self.clf = SVC(kernel="linear", C=2)

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

avaliables_classifiers = {
    "SVM": SVR,
    "LDA": LinearDiscriminantAnalysis
}

@register_training
class OneVsAll(Training):

    def __init__(self, classifier="LDA", **kargs):
        self.clf = classifier
        self.classifiers = []
        self.labels = []

    def prepareLabels(self, label, y):
        return list(map(lambda x : 1 if x == label else 0, y))

    def fit(self, X, y):
        self.labels = list(set(y))
        for label in self.labels:
            clf =SVC(kernel="linear", C=2, probability=True)
            clf.fit(X, self.prepareLabels(label, y))
            self.classifiers.append(clf)
        
        return OneVsAllClassifier(self.classifiers, self.labels)


    def load(self, filename) -> OneVsAllClassifier:
        return load(filename)
