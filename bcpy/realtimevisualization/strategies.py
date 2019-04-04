from .realtime import Realtime, register_realtime
from ..serve.flask import start_server
import requests
import socketio


@register_realtime
class WebPage(Realtime):
    def __init__(self):
        start_server()
        self.sio = socketio.Client()

    def start(self):
        self.sio.connect('http://localhost:5000')

    def stop(self):
        requests.post('http://localhost:5000/shutdown')

    def send_data(self, timestamp, eeg, channels):
        self.sio.emit(
            "eeg_data", {"eeg": eeg,
                         "channels": channels,
                         "timestamp": timestamp})
