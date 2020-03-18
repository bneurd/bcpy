import numpy as np
from . import feature_extract
from mne.time_frequency import psd_welch
from sklearn.preprocessing import StandardScaler


class BandExtract(feature_extract.FeatureExtract):
    AVALIABLE_BANDS = {
        "alpha": (8.0, 12.0),
        "beta": (12.0, 40.0),
        "gamma": (40.0, 100.0),
        "theta": (4.0, 8.0),
        "delta": (0.0, 4.0)
    }

    def __init__(self,
                 bands,
                 freqs_around=None,
                 standard_scaler=True,
                 average=False):
        self.bands = bands
        self.freqs_around = freqs_around
        self.standard_scaler = standard_scaler
        self.average = average

    def get_freq_range(self, band):
        if type(band) is str:
            return self._get_range_from_str(band)
        return self._get_freq_range_from_number(band)

    def _get_freq_range_from_number(self, band):
        freqs_around = self.freqs_around if self.freqs_around else 0.5
        min_freq = float(band) - freqs_around
        max_freq = float(band) + freqs_around
        return min_freq, max_freq

    def _get_range_from_str(self, band: str):
        if band in self.AVALIABLE_BANDS:
            return self.AVALIABLE_BANDS[band]

    def extract(self, raw):
        feature = []
        for band in self.bands:
            min_freq, max_freq = self.get_freq_range(band)
            psd, _ = psd_welch(raw, fmin=min_freq,
                               fmax=max_freq, verbose=False)

            band_all_channels = np.average(psd, axis=1)
            if self.average:
                feature.append([np.average(band_all_channels)])
            else:
                feature.append(band_all_channels)
        if self.standard_scaler:
            return StandardScaler().fit_transform(np.array(feature)).flatten()
        return feature
