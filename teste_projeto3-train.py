import numpy as np
from scipy.io import loadmat
from bcpy.features.psd import psd
from bcpy.learning import training
from bcpy.processing import bandfilter
from bcpy.acquisition import getdata_label

subject = 1


def get_custom_data():
    m_of_m = list()
    new_data = list()
    trial = list()
    for letter in 'abcd':
        print('Subject', subject, '/ Session', letter)
        data = loadmat('data/T0{:02d}{}.mat'.format(subject, letter))
        calc = list()
        for i in range(1, len(data['DIN_1'][3])):
            ids = data['DIN_1'][3][i - 1][0][0], data['DIN_1'][3][i][0][0]
            interval = ids[1] - ids[0]
            # interval more than 50 is other target
            if interval > 50:
                calc.append(ids)
        indexes = list()
        for i in range(1, len(calc)):
            first = calc[i - 1][1]
            last = calc[i][0]
            # difference more than 1000 qualify a trial
            if (last - first) > 1000:
                indexes.append((last, first))
        indexes.append((data['DIN_1'][3][-1][0][0], calc[-1][1]))
        # get the minor size of trial
        minor = min([(l - f) for l, f in indexes])
        m_of_m.append(minor)
        trial.append(np.array([data['eeg'][:, f:f+1205] for l, f in indexes]))

    print('Finished!')
    new_data = np.array(trial)

    print(new_data.shape)
    new_data = np.reshape(new_data, (100, 257, 1205))
    print(new_data.shape)

    for trial in new_data:
        yield trial.T


def get_custom_label():
    for letter in 'abcd':
        print('Subject', subject, '/ Session', letter)
        data = loadmat('data/T0{:02d}{}.mat'.format(subject, letter))
        labels = [l[0][0] for l in data['labels'][0]]
        print(labels)

    print('Finished!')

    labels = np.array(labels*5)

    for label in labels:
        yield label


data, labels = getdata_label(
    "Custom", get_data=get_custom_data, get_label=get_custom_label)
filter_buff1 = bandfilter(data, lo=5, hi=25, order=8, fs=250)
filter_buff2 = bandfilter(filter_buff1, lo=5, hi=25, order=8, fs=250)
filter_buff3 = bandfilter(filter_buff2, lo=5, hi=25, order=8, fs=250)
psds = psd(filter_buff3, fs=250)
classifier = training('OneVsAll', psds, labels, verbose=True)
classifier.save('model.joblib')
