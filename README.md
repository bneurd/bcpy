# BCPY

A simple library to handle all steps of a BCI system.

## Acquisition Data

This module handles the Acquisition from an EEG. At this moment, this module can handle the following types of connection with the EEG Board:

- LSL

### How to use

``` python
from bcpy.signalacquisition import getdata

from time import sleep

ConnectionProccess, data = getdata("LSL", board="openBCI",channels=["O1", "O2", "Oz"])

# wait untill first data arrive
while(not p.is_receiving_data()):
    pass

print("Stream started")
# set marker with label 2
data.set_marker(2)

# wait 2 seconds
sleep(2)

# set marker with label 1
data.set_marker(1)

# wait 2 seconds
sleep(2)

# close connection
ConnectionProccess.terminate()
print("data acquisition end")
print("\n\n\n")

# get values
timeStamp, eeg, markers = data.get_values()
```

### Visualize data on web broswer

bcpy `signalacquisition` modules start a web serve to handle the data visualization. this web server can be seen on `http://localhost:5000`