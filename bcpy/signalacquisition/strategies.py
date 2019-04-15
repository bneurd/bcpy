from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager
from .acquisition import Acquisition, register_acquisition, AcquisitionData
import os


@register_acquisition
class LSL(Acquisition):
    """Reciver using the protocol LSL to get data

    Parameters
    ----------
    - frequency: `int`
        frequency of transmission
    - channels: :obj:`list` of `str`
        list of eletrodos utilized on the experiment
    - marker_strategy: :obj:`MarkerStrategy`, optional
        stragey to get the markers from the experiment
    """

    def __init__(self,
                 visualizationOptions={
                     "visualization": "WebPage",
                     "numOfPackages": 250
                 },
                 **kwargs):
        super().__init__(visualizationOptions["visualization"])
        board = kwargs.get('board')
        self.channels = kwargs.get('channels')
        self.pkgsPerSec = visualizationOptions["numOfPackages"]
        frequency = kwargs.get('frequency')
        if not frequency:
            if board == "openBCI":
                if len(self.channels) < 8:
                    self.frequency = 250
                else:
                    self.frequency = 125
            else:
                # TODO: raise error
                pass

        self.recive_first_data = Value('i', 0)

    def is_receiving_data(self):
        return bool(self.recive_first_data.value)

    def terminate(self):
        self.get_data_process.terminate()
        self.visualization.stop()

    def get_data(self):
        """Get data from lsl protocol

        Return
        ------
        - multiprocessing.Process
            process geting data

        """

        BaseManager.register('AcquisitionData', AcquisitionData)
        manager = BaseManager()
        manager.start()
        inst = manager.AcquisitionData()
        self.get_data_process = Process(target=self.__get_data,
                                        args=(inst, self.recive_first_data))
        self.get_data_process.start()

        return self, inst

    def __get_data(self, data, recive_first_data):
        # connect to socket.io
        self.visualization.start()
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')

        try:
            inlet = StreamInlet(streams[0])
        except Exception as ex:
            raise ex

        interval = 1 / self.frequency * 1000
        last_time = -interval

        data_to_transmit = []
        timestamp_to_tramsmit = []
        pkg_count = 0
        while True:
            chunk, timestamp = inlet.pull_chunk()

            # sometimes... this loop is faster than chunk receiving
            if (timestamp):
                recive_first_data.value = 1
                for i in range(len(timestamp)):
                    time_now = last_time + interval
                    last_time = time_now

                    data_to_transmit.append(chunk[i])
                    timestamp_to_tramsmit.append(time_now)
                    pkg_count += 1

                    if pkg_count >= self.frequency/self.pkgsPerSec:
                        self.visualization.send_data(timestamp_to_tramsmit,
                                                     data_to_transmit,
                                                     self.channels,
                                                     self.frequency)
                        # os.system("mosquitto_pub -d -t game -m " + str(60))
                        data_to_transmit = []
                        timestamp_to_tramsmit = []
                        pkg_count = 0

                    data.add_data(time_now, chunk[i])