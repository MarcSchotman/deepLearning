import pickle
import random

import numpy as np


def generate_batch(data_dir: str, filenames: [str], station_id_pred, batch_size=3, t_train=7,
                   features_train=None,
                   t_pred=7, features_pred=None, padding=0, pad_value=99.0):
    """
    Generator to load data batch-wise. Formats data to matrix that is fed to the neural network.
    X contains the source Y contains the target.
    e.g for one week prediction X contains year calendar week 41,1,57, Y contains 42,2,58
    :param padding: number of timesteps to pad
    :param pad_value: this value is used for padding and will considered so by the network
    :param data_dir:  directory of pickle files
    :param filenames: names of files to load
    :param batch_size: batch_size
    :param t_train: Length of sequence to train on
    :param features_train: Number of features to train on
    :param t_pred: Length of sequence to predict
    :param station_id_pred: Station for which to predict
    :param features_pred: Amount of features to predict
    :return: two matrices:
    x_batch: (#batch,#seq_len_train,#features_train * #stations)
    y_batch: (#batch,#seq_len_pred, #features_pred)
    """
    if features_pred is None:
        features_pred = ['air_temperature']
    if features_train is None:
        features_train = ['air_temperature', 'humidity']
    if not isinstance(filenames, list):
        filenames = [filenames]

    # Yields batches as long as called by training procedure
    while True:
        random.shuffle(filenames)
        for f in filenames:
            file_content = pickle.load(open(data_dir + f + '.pickle', 'rb'))
            n_stations = len(file_content)
            t_max = len(file_content[station_id_pred][features_train[0]])
            n_batches = int(t_max / batch_size)

            for _ in range(n_batches):
                # Create tensors to store data + labels
                x_batch = np.zeros((batch_size, t_train + padding
                                    , n_stations, len(features_train))) * np.nan
                y_batch = np.zeros((batch_size, t_pred, len(features_pred))) * np.nan

                # Collect data for one batch
                for i_batch in range(batch_size):
                    # Choose a random time step within the file to start.
                    t_start = random.choice([n for n in range(0, t_max - (t_train + t_pred), 24)])
                    t_end = t_start + t_train
                    # Collect data for one time step
                    for t in range(t_start, t_end):

                        # Collect data for all stations
                        for i_station, station_id in enumerate(file_content.keys()):

                            # Collect measurements for all features
                            for i_feature, feature in enumerate(features_train):
                                x_batch[i_batch, t - t_start, i_station, i_feature] = file_content[station_id][feature][
                                    t]

                    # Collect label (prediction) for that sample by choosing the following sequence
                    for t in range(t_end, t_end + t_pred):
                        # Collect data for selected station
                        for i_feature, feature in enumerate(features_pred):
                            y_batch[i_batch, t - t_end, i_feature] = file_content[station_id_pred][feature][t]

                x_batch[np.isnan(x_batch)] = pad_value

                # Reshape to tensor keras wants
                x_batch = np.reshape(x_batch, (batch_size, t_train + padding, n_stations * len(features_train)))
                y_batch = np.reshape(y_batch, (batch_size, t_pred, 1))
                yield x_batch, y_batch


if __name__ == '__main__':
    x, y = next(
        generate_batch('../data/RADIUS200KM_PROCESSED/', ['2017'], '724699-03065', batch_size=1, t_train=3, t_pred=3,
                       padding=3,pad_value=99.0))
    print('X :', x)
    print('Y :', y)
