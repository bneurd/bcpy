# BCPY

A simple library to handle all steps of a BCI system.

## Acquisition Data

This module handles the Acquisition from an EEG. At this moment, this module can handle the following types of connection with the EEG Board:

- LSL

### How to use

``` python
from bcpy.acquisition import getdata
from bcpy.realtimevisualization import realtimevisualization
from bcpy.utils import makebuff, flow
from bcpy.processing import apply_filter

options = {
    "channels": ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2"],
    "fs": 256
}

data = getdata("LSL")
buff = makebuff(data, 256)
# apply bandpass filter [5-50]
filter_buff = apply_filter(buff, lo=5, hi=50, fs=256)
buffvis = realtimevisualization(
    "WebPage", filter_buff, options)


flow(buffvis)
```

### Visualize data

For now, the GUI to visualize the data is on the follow repository [https://github.com/igornfaustino/realtime-eeg-dashboard](https://github.com/igornfaustino/realtime-eeg-dashboard)