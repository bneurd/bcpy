from acquisition_strategy import AcquisitionStrategy
# from multiprocessing import Process, Manager, Queue


class DataAcquisition():
    def __init__(self, strategy: AcquisitionStrategy):
        self.strategy = strategy

    def save_data(self):
        self.strategy.save_data()
