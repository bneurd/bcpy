from bcpy.signalacquisition import getdata
from bcpy.realtimevisualization import realtimevisualization
from bcpy.signalutils.buffer import makebuff

options = {
    "channels": ["O1", "O2"],
    "fs": 128
}

data = getdata("LSL", board="openBCI", n_channels=2)
buff = realtimevisualization(
    "WebPage", makebuff(data, 128), options)

# rawData = realtimevisualization(
#     "WebPage", getdata("LSL", board="openBCI", n_channels=2), options)


while(True):
    print(len(next(buff)))
