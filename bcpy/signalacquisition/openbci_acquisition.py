from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process
from bcpy.serve.flask import start_server
import socketio


class OpenBCIAcquisition():
    """Reciver using the protocol LSL to get data from OpenBCI

    Parameters
    ----------
    frequency: `int`
        frequency of transmission
    channels: :obj:`list` of `str`
        list of eletrodos utilized on the experiment
    marker_strategy: :obj:`MarkerStrategy`, optional
        stragey to get the markers from the experiment
    """

    def __init__(self, frequency, channels, marker_stragy=None):
        self.frequency = frequency
        self.channels = channels
        self.marker_stragy = marker_stragy
        start_server()
        self.sio = socketio.Client()

    def get_data(self, print_data=False):
        """Get data from lsl protocol

        Parameters
        ----------
        print_data: `boolean`, optional
            show data on terminal
        """

        try:
            if not self.marker_stragy:
                p = Process(target=self.__save_data_without_markers,
                            args=(print_data,))
                p.start()
        except KeyboardInterrupt:
            p.terminate()

    def __save_data_without_markers(self, print_data):
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')

        try:
            inlet = StreamInlet(streams[0])
        except Exception as ex:
            print(ex)
        # eeg timestamp, eeg data channels, markerss
        self.__data = [[], [], []]
        interval = 1 / self.frequency * 1000
        last_time = -interval

        self.sio.connect('http://localhost:5000')
        data_to_transmit = []
        pkg_count = 0
        while True:
            chunk, timestamp = inlet.pull_chunk()

            # sometimes... this loop is faster than chunk receiving
            if (timestamp):
                for i in range(len(timestamp)):
                    time_now = last_time + interval
                    self.__data[0].append(time_now)
                    last_time = time_now
                    self.__data[1].append(chunk[i])

                    data_to_transmit.append(chunk[i])
                    pkg_count += 1

                    if pkg_count >= self.frequency/2:
                        self.sio.emit("eeg_data", {"eeg": data_to_transmit})
                        data_to_transmit = []
                        pkg_count = 0

                    if (print_data):
                        print(chunk[i])
