from bcpy.acquisition import getdata
from bcpy.realtimevisualization import realtimevisualization
from bcpy.utils.buffer import makebuff
from bcpy.processing import apply_filter, notch

options = {
    "channels": ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2"],
    "fs": 256
}

data = getdata("LSL")
buff = makebuff(data, 256)
filter_buff = apply_filter(buff, lo=5, hi=50, fs=128)
buffvis = realtimevisualization(
    "WebPage", filter_buff, options)


while(True):
    next(buffvis)
