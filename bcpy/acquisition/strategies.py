import pylsl
from . import acquisition


@acquisition.register_acquisition
class LSL(acquisition.Acquisition):
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

    def __init__(self, fs=128):
        self.frequency = fs

    def is_receiving_data(self):
        return bool(self.recive_first_data.value)

    def terminate(self):
        self.get_data_process.terminate()
        self.visualization.stop()

    def get_data(self):
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
