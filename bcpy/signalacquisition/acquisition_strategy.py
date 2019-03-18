from abc import ABC, abstractmethod


class AcquisitionStrategy(ABC):
    @abstractmethod
    def save_data(self):
        pass
