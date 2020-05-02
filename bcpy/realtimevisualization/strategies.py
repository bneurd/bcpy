from . import realtime
from ..serve import flask
import socketio
import json
import numpy as np
import time


@realtime.register_realtime
class WebPage(realtime.Realtime):
    """ Start a webpage GUI, this is also used to send data to WEBVIEW

    * In the future will be separeted the webpage from the webview

    Parameters
    ----------
    - options : config `dict` with:
        - `channels` names in `str`
        - `fs` in `number`
    """

    greater_diff = 1
    last_call_time = 0
    last_call_data_len = 0
    max_of_last_calls = 1
    calls_count = 0

    def __init__(self, options):
        super().__init__(options)
        self.server_process = flask.start_server()
        self.sio = socketio.Client()

    def start(self):
        self.sio.connect('http://localhost:5000')

    def stop(self):
        self.sio.disconnect()
        self.server_process.terminate()

    def send_data(self, eeg):
        self.sio.emit(
            "eeg_data", json.dumps({"eeg": eeg,
                                    "channels": self.channels,
                                    "fs": self.fs,
                                    "timestamp": time.time() * 1000
                                    }))

    def __normalize_time(self, first, data):
        time_now = time.time()
        if not first:
            diff = time_now - self.last_call_time - \
                (self.greater_diff/self.fs) * self.last_call_data_len
            print("diff: ", diff)
            if diff > self.greater_diff:
                self.greater_diff = diff
            if diff > self.max_of_last_calls:
                self.max_of_last_calls = diff
        self.last_call_time = time_now
        self.last_call_data_len = len(data)
        self.calls_count += 1

        if self.calls_count >= 10:
            self.calls_count = 0
            self.greater_diff = self.max_of_last_calls
            self.max_of_last_calls = 1

        print("greater diff: ", self.greater_diff)

    def show_realtime_data(self, data, minimum_time=None):
        time_max = minimum_time if minimum_time and minimum_time > 1 else 1
        # self.__normalize_time(first, data)
        if (len(np.array(data).shape) == 1):
            self.send_data(data)
        else:

            for each_data in data:
                begin = time.time()
                if (isinstance(each_data, np.ndarray)):
                    self.send_data(each_data.tolist())
                else:
                    self.send_data(each_data)
                # wait for 1/fs... but consider the send delay
                time_remain = (time_max/self.fs) - \
                    (time.time() - begin)
                if time_remain < 0:
                    time_remain = 0
                time.sleep(time_remain)
