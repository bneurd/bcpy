from bcpy.signalacquisition.data_acquisition import DataAcquisition
from bcpy.signalacquisition.acquisition_strategy import AcquisitionStrategy
from bcpy.signalacquisition.openbci_strategy import OpenBCIStrategy

if __name__ == "__main__":
    acquisition_strategy = AcquisitionStrategy()
    openbci = OpenBCIStrategy()
    data_acquisition = DataAcquisition()
