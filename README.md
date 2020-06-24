# BCPY

A simple library to handle all steps of a BCI system.

# Installation guide

the toolkit depends on pipenv to control the environment on a simple way. To install pipenv just go to the [official github page](https://github.com/pypa/pipenv).

To start the development environment just type `pipenv shell`, after that you'll be inside an virtual environment with everything you need to run the project.

## How to use

The following is an simple example on how the toolkit works

### Data Acquisition

The data is get by the `LSL` protocol and created an window with 3 seconds of the data.

```python
import numpy as np
from bcpy.acquisition import getdata
from bcpy.base import create_window, flow, create_eeg_object

data = getdata("LSL")
buff_win = create_window(data, 768, 512)
eeg_obj = create_eeg_object(buff_win, fs=250, channels=[
                            "1", "2", "3", "4", "5", "6", "7", "8"])
```

### Pre process

Apply an band-pass filter with 5-50hz (the filter is applied 3 times to better results)

```python
from bcpy.processing import bandfilter

filter_buff1 = bandfilter(eeg_obj, lo=5, hi=50)
filter_buff2 = bandfilter(filter_buff1, lo=5, hi=50)
filter_buff3 = bandfilter(filter_buff2, lo=5, hi=50)
```

### Feature extraction

To extract feature you need to define a list with all extract methods that will be apply to each window. The return of the extract method will be an list with all the features.

```python
from bcpy.features import extract
from bcpy.features.strategies import BandExtract

extract_methods = [
    BandExtract(
        ['alpha', 'beta', 'gamma', 'delta', 'theta'],
        average=True
    )
]

features = extract(filter_buff3, extract_methods)
```

### Flow

To make the flow defined works, you need to call the flow function as the last thing.

The flow function by default just executes the other steps, but you can pass a custom function to apply some kind of analysis on the data, like showed on the code bellow. This custom function compares the value between the all the bands extracted and display the percent of how much the alpha band is bigger than the rest.

```
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
```
