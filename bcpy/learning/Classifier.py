from joblib import dump
import numpy as np


class Classifier():
    def __init__(self, clf):
        self.clf = clf

    def predict(self, X):
        pass

    def save(self, filename):
        dump(self.clf, filename)

class OneVsAllClassifier(Classifier):
    def __init__(self, clfs, labels):
        self.clfs = clfs
        self.labels = labels
        self.clf = self
    
    def score_result(self, right, wrong):
        total = right + wrong
        return right / total
    
    def score(self, X, y):
        votes = []
        right = 0
        wrong = 0
        for clf in self.clfs:
            print(clf.predict(X))
            votes.append(clf.predict(X))
        votes = np.array(votes)
        for idx, vote in enumerate(votes.T):
            max_index = np.argmax(vote)
            predicted_label = self.labels[max_index]
            if predicted_label == y[idx]:
                right += 1
            else:
                wrong += 1
            # break
        return self.score_result(right, wrong)
    
    def save(self, filename):
        dump(self.clf, filename)
        
