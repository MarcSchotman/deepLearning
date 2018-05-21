import pickle
import random

import numpy as np


def generate_batch(data_dir: str, filenames: [str], batches_per_file=20, batch_size=3, seq_len_train=7,
                   features_train=None,
                   seq_len_pred=7, station_id_pred=0, features_pred=None, t_max=365):
    """
    Generator to load data batch-wise. Formats data to matrix that is fed to the neural network.
    X contains the source Y contains the target.
    e.g for one week prediction X contains year calendar week 41,1,57, Y contains 42,2,58
    :param t_max: highest possible time step (within one file)
    :param data_dir:  directory of pickle files
    :param filenames: names of files to load
    :param batches_per_file: number of entries per file
    :param batch_size: batch_size
    :param seq_len_train: Length of sequence to train on
    :param features_train: Number of features to train on
    :param seq_len_pred: Length of sequence to predict
    :param station_id_pred: Station for which to predict
    :param features_pred: Amount of features to predict
    :return: two matrices:
    x_batch: (#batch,#seq_len_train,#features_train * #stations)
    y_batch: (#batch,#seq_len_pred, #features_pred)
    """
    if features_pred is None:
        features_pred = ['air_temperature']
    if features_train is None:
        features_train = ['air_temperature']
    if not isinstance(filenames, list):
        filenames = [filenames]

    # Randomly select a file
    while True:
        filename = random.choice(filenames)
        file_content = pickle.load(open(data_dir + filename + '.pickle', 'rb'))
        n_stations = len(file_content)

        if station_id_pred is None:
            # TODO maybe replace this with the station that is closest to delft
            station_id_pred = list(file_content.keys())[0]

        for _ in range(batches_per_file):
            # Create tensors to store data + labels
            x_batch = np.zeros((batch_size, seq_len_train
                                , n_stations, len(features_train)))
            y_batch = np.zeros((batch_size, seq_len_pred, len(features_pred)))

            # Collect data for one batch
            for i_batch in range(batch_size):
                # Choose a random time step within the file to start
                t_start = random.choice([n for n in range(t_max - seq_len_train)])
                t_end = t_start + seq_len_train
                # Collect data for one time step
                for t in range(t_start, t_end):

                    # Collect data for all stations
                    for i_station, station_id in enumerate(file_content.keys()):

                        if station_id is station_id_pred: continue

                        # Collect measurements for all features
                        for i_feature, feature in enumerate(features_train):
                            # TODO the data is hourly while the function assumes daily
                            x_batch[i_batch, t - t_start, i_station, i_feature] = file_content[station_id][feature][t]

                # Collect label (prediction) for that sample by choosing the following sequence
                for t in range(t_end, t_end + seq_len_pred):
                    # Collect data for selected station
                    for i_feature, feature in enumerate(features_pred):
                        y_batch[i_batch, t - t_end, i_feature] = file_content[station_id_pred][feature][t]

            # Reshape to tensor keras wants
            x_batch = np.reshape(x_batch, (batch_size, seq_len_train, n_stations * len(features_train)))
            y_batch = np.reshape(y_batch, (batch_size, seq_len_pred))
            yield x_batch, y_batch
