from joblib import dump


class Classifier():
    def __init__(self, clf):
        self.clf = clf

    def predict(self, X):
        pass

    def save(self, filename):
        dump(self.clf, filename)
