import numpy as np
import os
import scipy
import scipy.io
from bcpy.acquisition import getdata_label
from bcpy.processing import bandfilter
from bcpy.features.psd import psd
from bcpy.learning import training
from bcpy.base import create_eeg_object, plot_psd


def load_data(path):
    data = scipy.io.loadmat(path)['Data']
    data = data['EEG'][0][0]
    data = np.expand_dims(data.T, axis=1)

    return data


def get_custom_data():
    subject = 1
    DIR_PATH = os.path.dirname(__file__)
    for session in (2,):
        fpath = os.path.join(DIR_PATH, "multi",
                             "Sub%d_%d_multitarget.mat" % (subject, session))

        epochs = load_data(fpath)
        for epoch in epochs:
            yield epoch.T


def load_label(path):
    data = scipy.io.loadmat(path)['Data']
    t_freqs = ['%s' % str(t) for t in data['TargetFrequency'][0][0][0]]
    f_freqs = data['FlickeringFrequencies'][0][0].flatten()
    f_freqs = ['%s' % str(f) for f in f_freqs]

    f_freqs = set.intersection(set(t_freqs), set(f_freqs))

    return t_freqs


def get_custom_label():
    subject = 1
    DIR_PATH = os.path.dirname(__file__)
    for session in (2,):
        fpath = os.path.join(DIR_PATH, "multi",
                             "Sub%d_%d_multitarget.mat" % (subject, session))

        labels = load_label(fpath)
        for label in labels:
            yield label


data, labels = getdata_label(
    "Custom", get_data=get_custom_data, get_label=get_custom_label)
objs = create_eeg_object(data, 256, ["o2"])
# filter_buff1 = bandfilter(objs, lo=5, hi=50)
# filter_buff2 = bandfilter(filter_buff1, lo=5, hi=50)
# filter_buff3 = bandfilter(filter_buff2, lo=5, hi=50)
psds = psd(objs)
# x = plot_psd(psds)
# classifier = training('OneVsAll', x, labels, verbose=True)
# classifier.save('model.joblib')
print(next(psds))
