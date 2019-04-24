from bcpy.signalacquisition import getdata
from bcpy.realtimevisualization import realtimevisualization

options = {
    "channels": ["Fp1", "Fp2", "C3", "C4", "T5", "T6", "O1", "O2"],
    "fs": 125
}

data = realtimevisualization("WebPage", getdata("LSL", board="openBCI"), options)


# while(True):
#     print(next(data, None))
