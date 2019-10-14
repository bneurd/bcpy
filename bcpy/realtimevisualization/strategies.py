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

    def show_realtime_data(self, data):
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
                time_remain = (1/self.fs) - (time.time() - begin)
                time.sleep(time_remain)
