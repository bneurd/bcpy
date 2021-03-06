import types
import numpy as np
from abc import ABC, abstractmethod


class FeatureExtract(ABC):
    @abstractmethod
    def extract(data):
        pass


def extract(gen: types.GeneratorType, strategies: list()):
    while True:
        raw_data = next(gen)
        features = []
        for strategy in strategies:
            if not issubclass(type(strategy), FeatureExtract):
                raise Exception('Feature Extraction function invalid')
            feature = strategy.extract(raw_data)
            features.append(feature)
        yield np.array(features).flatten()
