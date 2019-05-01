from bcpy.signalacquisition import getdata
from bcpy.realtimevisualization import realtimevisualization

options = {
    "channels": ["O1", "O2"],
    "fs": 128
}

rawData = realtimevisualization(
    "WebPage", getdata("LSL", board="openBCI", n_channels=2), options)


while(True):
    print(next(rawData, None))
