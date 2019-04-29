from bcpy.signalacquisition import getdata
from bcpy.realtimevisualization import realtimevisualization

options = {
    "channels": ["Fp1", "Fp2", "C3",
                 "C4", "T5", "T6", "O1", "O2"
                 ],
    "fs": 250
}

rawData = realtimevisualization(
    "WebPage", getdata("LSL", board="openBCI", n_channels=8), options)


while(True):
    next(rawData, None)
