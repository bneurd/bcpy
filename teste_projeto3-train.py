import os
import numpy as np
from re import search
from subprocess import getoutput as gop
from bcpy.features import extract
from bcpy.features.strategies import PSD
from bcpy.learning import training
from bcpy.base import create_eeg_object
from bcpy.processing import drop_channels, car
from bcpy.acquisition import getdata_label

USELESS_CHANNELS = ['x', 'nd', 'y']
USEFULL_CHANNELS = ["c3", "cp4", "cp5"]


class CustomAcquisition():
    def __init__(self, path):
        self.subjects = []
        self.ch_names = []
        self.labels = []
        self.folder_path = path
        self.load_data_with_label()

    def load_data_with_label(self):
        create_ch_name = False
        subjects = []
        labels = []

        # get all dirs inside folder
        folder = gop('ls {}'.format(self.folder_path)).split('\n')
        # for all dir insider folder
        for types in folder:
            if (not os.path.isdir('{}/{}'.format(self.folder_path, types))):
                continue
            label_search = search('^co2(?P<label>\w{1})', types)

            files = gop('ls {}/{}'.format(self.folder_path, types)).split('\n')
            # 2ª dimensão dos dados contendo as sessões (trials)
            trials = list()

            # for all file in files
            for f in files:
                if (label_search.group("label") == "a"):
                    labels.append(1)
                else:
                    labels.append(0)
                arquivo = open('{}/{}/{}'.format(self.folder_path, types, f))
                text = arquivo.readlines()
                # 3ª dimensão dos dados contendo os canais (eletrodos)
                chs = list()
                # 4ª dimensão dos dados contendo os valores em milivolts
                values = list()
                # for each line inside a file
                for line in text:
                    # ex: "# FP1 chan 0"
                    # look if this line is a new eletrodo info
                    t = search('(?P<ch_name>\w{1,3}) chan \d{1,2}', line)
                    # ex: "0 FP1 0 -8.921"
                    # or if is a data line
                    p = search(
                        '^\d{1,3}\ \w{1,3}\ \d{1,3}\ (?P<value>.+$)', line)

                    # if has a eeg data
                    if p:
                        values.append(float(p.group('value')))
                    # mudou para outro eletrodo
                    elif t:
                        if values:
                            chs.append(values)
                            values = list()
                        if not create_ch_name:
                            self.ch_names.append(t.group('ch_name').lower())

                # end for line
                # append last channel
                chs.append(values)
                create_ch_name = True

                # append all channels to one trial
                trials.append(chs)
                arquivo.close()
            # append all trials to one subject
            subjects.append(trials)
            self.subjects = np.array(subjects)
            self.labels = np.array(labels)

    def get_data(self):
        trials = self.subjects.reshape(600, 64, 256)
        for trial in trials:
            yield trial.T

    def get_label(self):
        for label in self.labels:
            yield label


test_data = CustomAcquisition('SMNI_CMI_TRAIN')
data, labels = getdata_label(
    "Custom", get_data=test_data.get_data, get_label=test_data.get_label)
objs = create_eeg_object(data, 256, channels=test_data.ch_names)
dropped_channels_objs = drop_channels(objs, USELESS_CHANNELS)
car_objs = car(dropped_channels_objs, ref_channels=USEFULL_CHANNELS)
features = extract(car_objs, [PSD()])
classifier = training('SVM', features, labels, verbose=True)
classifier.save('model.joblib')
