import numpy as np
import os
import scipy
import scipy.io
from bcpy.acquisition import getdata_label
from bcpy.processing import bandfilter
from bcpy.features.psd import psd
from bcpy.learning import training


def load_data(path):
    data = scipy.io.loadmat(path)['Data']
    data = data['EEG'][0][0]
    data = np.expand_dims(data.T, axis=1)

    return data


def get_custom_data():
    subject = 1
    DIR_PATH = os.path.dirname(__file__)
    for session in (1,):
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

    return list(map(lambda x: 1 if x == '8.2' else 0, t_freqs))


def get_custom_label():
    subject = 1
    DIR_PATH = os.path.dirname(__file__)
    for session in (1,):
        fpath = os.path.join(DIR_PATH, "multi",
                             "Sub%d_%d_multitarget.mat" % (subject, session))

        labels = load_label(fpath)
        for label in labels:
            yield label


data, labels = getdata_label(
    "Custom", get_data=get_custom_data, get_label=get_custom_label)
filter_buff1 = bandfilter(data, lo=5, hi=50, order=8)
filter_buff2 = bandfilter(filter_buff1, lo=5, hi=50, order=8)
filter_buff3 = bandfilter(filter_buff2, lo=5, hi=50, order=8)
psds = psd(filter_buff3)
classifier = training('SVM', psds, labels, verbose=True)
classifier.save('model.joblib')
