import numpy as np
from bcpy.acquisition import getdata
from bcpy.base import create_window, flow, create_eeg_object
from bcpy.processing import bandfilter
from bcpy.features import extract
from bcpy.features.strategies import BandExtract
from bcpy.realtimevisualization import realtimevisualization

data = getdata("LSL")
buff_win = create_window(data, 768, 512)
eeg_obj = create_eeg_object(buff_win, fs=250, channels=[
                            "1", "2", "3", "4", "5", "6", "7", "8"])
filter_buff1 = bandfilter(eeg_obj, lo=5, hi=50)
filter_buff2 = bandfilter(filter_buff1, lo=5, hi=50)
filter_buff3 = bandfilter(filter_buff2, lo=5, hi=50)

viz = realtimevisualization('WebPage',
                            filter_buff3,
                            {
                                "intersection": 512,
                                "fs": 250,
                                "channels": [
                                    "1", "2", "3", "4", "5", "6", "7", "8"
                                ]
                            })

features = extract(viz, [BandExtract(
    ['alpha', 'beta', 'gamma', 'delta', 'theta'], average=True)])


def scala100(maxValue, minValue):
    return minValue*100/maxValue


def process(feature):
    maxIndex = np.argmax(feature)

    if (maxIndex == 0):
        secondMaxIndex = np.argmax(feature[1:])+1
        maxValue = feature[maxIndex]
        minValue = feature[secondMaxIndex]
        print(scala100(maxValue, minValue))
    else:
        print(0)


flow(features, function=process)
