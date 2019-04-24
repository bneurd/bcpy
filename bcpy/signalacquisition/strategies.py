from pylsl import StreamInlet, resolve_stream
import threading
from .acquisition import Acquisition, register_acquisition


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
                 channels=["Fp1", "Fp2", "C3", "C4", "T5", "T6", "O1", "O2"],
                 **kwargs):
        board = kwargs.get('board')
        self.channels = channels
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

    def is_receiving_data(self):
        return bool(self.recive_first_data.value)

    def terminate(self):
        self.get_data_process.terminate()
        self.visualization.stop()

    def get_data(self):
        """Get data from lsl protocol

        Return
        ------
        - 

        """

        t = threading.Thread(target=self.__get_data_thread)
        t.start()
    
    def __get_data_thread(self):
        self.data = self.__get_data()

    def __get_data(self):
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')

        try:
            inlet = StreamInlet(streams[0])
        except Exception as ex:
            raise ex

        interval = 1 / self.frequency * 1000
        last_time = -interval

        while True:
            chunk, timestamp = inlet.pull_chunk()

            # sometimes... this loop is faster than chunk receiving
            if (timestamp):
                for i in range(len(timestamp)):
                    time_now = last_time + interval
                    last_time = time_now

                    yield(chunk[i])
