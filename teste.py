import numpy as np
from bcpy.acquisition import getdata
from bcpy.base import create_window, flow
from bcpy.processing import bandfilter
from bcpy.features.psd import psd, band_extract
from bcpy.realtimevisualization import realtimevisualization

data = getdata("LSL")
buff_win = create_window(data, 768, 512)
filter_buff1 = bandfilter(buff_win, lo=5, hi=50, order=8)
filter_buff2 = bandfilter(filter_buff1, lo=5, hi=50, order=8)
filter_buff3 = bandfilter(filter_buff2, lo=5, hi=50, order=8)
realtime_data = realtimevisualization(
    "WebPage", filter_buff3, {
        "channels": ["01", "02", "03", "04", "05", "06", "07", "08"],
        "fs": 256,
        "intersection": 512
    })
psd_buff = psd(realtime_data, 256, average=True)


def scala100(maxValue, minValue):
    return minValue*100/maxValue


def process(psd_value):
    f, psd_values = psd_value
    bands = [0, 0, 0, 0]
    bands[0] = band_extract(f, psd_values, 8, 12)
    bands[1] = band_extract(f, psd_values, 5, 7)
    bands[2] = band_extract(f, psd_values, 12, 30)
    bands[3] = band_extract(f, psd_values, 25, 100)

    maxIndex = np.argmax(bands)

    if (maxIndex == 0):
        secondMaxIndex = np.argmax(bands[1:])+1
        maxValue = bands[maxIndex]
        minValue = bands[secondMaxIndex]
        print(scala100(maxValue, minValue))
    else:
        print(0)


flow(psd_buff, function=process)
