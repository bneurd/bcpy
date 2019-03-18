from bcpy.signalacquisition.acquisition_strategy import AcquisitionStrategy
from pylsl import StreamInlet, resolve_stream


class OpenBCIStrategy(AcquisitionStrategy):
    """Reciver using the protocol LSL to get data from OpenBCI

    Parameters
    ----------
    frequency: int
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

    def save_data(self):
        if not self.marker_stragy:
            self.save_data_without_markers()

    def save_data_without_markers(self):
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')

        inlet = StreamInlet(streams[0])
        # eeg timestamp, eeg data channels, markers
        data = [[], [], []]
        interval = 1 / self.frequency * 1000
        last_time = -interval

        while True:
            chunk, timestamp = inlet.pull_chunk()
            # sometimes... this loop is faster than chunk receiving
            if (timestamp):
                for i in range(len(timestamp)):
                    time_now = last_time + interval
                    data[0].append(time_now)
                    last_time = time_now
                    data[1].append(chunk[i])
