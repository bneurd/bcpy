import time
import pylsl
import types
import json
from . import acquisition


@acquisition.register_acquisition
class LSL(acquisition.Acquisition):
    """Reciver using the protocol LSL to get data

    Parameters
    ----------
    frequency: `int`
        frequency of transmission
    channels: :obj:`list` of `str`
        list of eletrodos utilized on the experiment
    """

    def __init__(self, fs: int = 128):
        self.frequency = fs

    def terminate(self):
        """ Stop receive data
        """
        self.get_data_process.terminate()
        self.visualization.stop()

    def get_data(self) -> types.GeneratorType:
        """ Resolve a lsl stream of type 'EEG'

        Yield
        -----
        data: :obj:`list` of n_channels
            Data for all channels on one interation

        Raises
        ------
        Exception:
            Fails to resolve data from stream
        """
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = pylsl.resolve_stream('type', 'EEG')

        try:
            inlet = pylsl.StreamInlet(streams[0])
        except Exception as ex:
            raise ex

        while True:
            chunk, timestamp = inlet.pull_chunk()

            # sometimes... this loop is faster than chunk receiving
            if (timestamp):
                for i in range(len(timestamp)):
                    yield(chunk[i])


@acquisition.register_acquisition
class FileBuffer(acquisition.Acquisition):
    def __init__(self, filename: str = 'data.json'):
        self.filename = filename

    def terminate(self):
        """ Stop receive data
        """
        self.get_data_process.terminate()
        self.visualization.stop()

    def get_data(self) -> types.GeneratorType:
        with open(self.filename) as source:
            data_structure = json.load(source)
            fs = data_structure["frequency"]
            data = data_structure["data"]
            for data_per_timestamp in data:
                yield data_per_timestamp['data']
                time.sleep(1/fs)
