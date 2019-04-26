from .realtime import Realtime, register_realtime
from ..serve.flask import start_server
import threading
import requests
import socketio
import json


@register_realtime
class WebPage(Realtime):
    def __init__(self, options):
        super().__init__(options)
        start_server()
        self.sio = socketio.Client()

    def start(self):
        self.sio.connect('http://localhost:5000')

    def stop(self):
        requests.post('http://localhost:5000/shutdown')

    def send_data(self, eeg):
        # print("oi")
        self.sio.emit(
            "eeg_data", json.dumps({"eeg": eeg,
                                    "channels": self.channels,
                                    "fs": self.fs}))

    def show_realtime_data(self, dataIter):
        t = threading.Thread(
            target=self.__show_realtime_data_thread, args=(dataIter,))
        t.start()

    def __show_realtime_data_thread(self, dataIter):
        self.data = self.__show_realtime_data(dataIter)

    def __show_realtime_data(self, dataIter):
        while(True):
            data = next(dataIter)
            self.send_data(data)
            yield(data)
