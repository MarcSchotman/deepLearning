import pickle

import numpy as np


def load_data(data_dir, years=(2008, 2017), n_entries_per_file=365, batch_size=3, seq_len_train=7,
              features_train=None,
              seq_len_pred=7, station_id_pred=0, features_pred=None):
    if features_pred is None:
        features_pred = ['air_temperature']
    if features_train is None:
        features_train = ['air_temperature']
    years = [str(y) for y in range(years[0], years[1])]
    for year in years:
        file_content = pickle.load(open(data_dir + year + '.pickle', 'rb'))
        # TODO we should shuffle the data somewhere
        for _ in range(n_entries_per_file):
            n_stations = len(file_content)
            x_batch = np.zeros((batch_size, seq_len_train
                                , n_stations, len(features_train)))
            y_batch = np.zeros((batch_size, seq_len_pred, len(features_pred)))
            for i in range(batch_size):
                for j in range(seq_len_train):
                    for k, station_id in enumerate(file_content.keys()):
                        for l, feature in enumerate(features_train):
                            x_batch[i, j, k, l] = file_content[station_id][feature][j]
                np.reshape(x_batch, (batch_size, seq_len_train, n_stations * len(features_train)))
                for j in range(seq_len_pred):
                    for k, feature in enumerate(features_pred):
                        y_batch[i, j, k] = file_content[str(station_id_pred)][j]
            yield x_batch, y_batch

