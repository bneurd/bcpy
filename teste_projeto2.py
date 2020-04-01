import numpy as np
import os
import scipy
import scipy.io
from bcpy.acquisition import getdata_label
from bcpy.processing import bandfilter
from bcpy.features import extract
from bcpy.features.strategies import BandExtract
from bcpy.learning import training
from bcpy.base import create_eeg_object


def load_data(path):
    data = scipy.io.loadmat(path)['Data']
    data = data['EEG'][0][0]
    data = np.expand_dims(data.T, axis=1)

    return data


subject = 2
session = 1


def get_custom_data():
    DIR_PATH = os.path.dirname(__file__)
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
    DIR_PATH = os.path.dirname(__file__)
    fpath = os.path.join(DIR_PATH, "multi",
                         "Sub%d_%d_multitarget.mat" % (subject, session))

    labels = load_label(fpath)
    for label in labels:
        yield label


data, labels = getdata_label(
    "Custom", get_data=get_custom_data, get_label=get_custom_label)
objs = create_eeg_object(data, 256, ["o2"])
filter_buff1 = bandfilter(objs, lo=5, hi=50)
filter_buff2 = bandfilter(filter_buff1, lo=5, hi=50)
filter_buff3 = bandfilter(filter_buff2, lo=5, hi=50)
features = extract(filter_buff3, [BandExtract([6, 7, 7.5, 8.2], 0.5)])
classifier = training('SVM', features, labels, verbose=True)
classifier.save('model.joblib')
