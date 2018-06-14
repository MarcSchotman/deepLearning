import numpy as np

_MISSING_VALUE = 999


def estimate_stats(generator, n_batches, features):
    """
    Estimates mean and stddev of dataset excluding missing data.
    :param generator: generator that loads dataset batchwise
    :param n_batches: number of batches
    :return: (mean,stddev)
    """
    nr_features = len(features)
    mean_sum = np.zeros((nr_features,), dtype=float)
    std_sum = np.zeros((nr_features,), dtype=float)

    mean_est = np.zeros((nr_features,), dtype=float)
    std_est = np.zeros((nr_features,), dtype=float)

    for i in range(n_batches):
        x, _ = next(generator)
        # reshape
        batch_size, seq_len, features_stations = x.shape
        stations_len = int(features_stations / nr_features)

        x = np.reshape(x, (batch_size, seq_len, stations_len, nr_features))

        for index_feature in range(nr_features):
            valid_idx = (x[:, :, :, index_feature] != _MISSING_VALUE)
            mean_sum[index_feature] += np.mean(x[valid_idx, index_feature], axis=0)
            std_sum[index_feature] += np.std(x[valid_idx, index_feature], axis=0)

            mean_est[index_feature] = mean_sum[index_feature] / n_batches
            std_est[index_feature] = std_sum[index_feature] / n_batches

    #       print(mean_est[0], mean_est[1])

    # print(mean_est[0], mean_est[1])
    return mean_est, std_est


def normalize(batch, mean, std, d):
    """
    Normalize batch by taking into account missing values.
    :param batch: tensor(#batch_size,#seq_len,#features*#stations)
    :param mean: mean of dataset
    :param std: standard deviation dataset
    :param d: Number of features
    :return: normalized batch: tensor(#batch_size,#seq_len,#features*#stations)
    """
    # reshape vector in order to apply feature specific means and std
    batch_size, seq_len, features_stations = batch.shape
    stations_len = int(features_stations / d)

    batch = np.reshape(batch, (batch_size, seq_len, stations_len, d))

    for index_feature in range(d):
        missing_idx = (batch[:, :, :, index_feature] == _MISSING_VALUE)
        valid_idx = (batch[:, :, :, index_feature] != _MISSING_VALUE)

        batch[valid_idx] -= mean[index_feature]
        batch[valid_idx] /= std[index_feature]
        batch[missing_idx] = 0
    # reshape back to original
    batch = np.reshape(batch, (batch_size, seq_len, stations_len * d))
    return batch


def normalize_generator(generator, mean, std, d_train, d_predict):
    """
    Generator to normalize batchwise before feeding it to the network.
    :param generator: generator that loads dataset batchwise
    :param mean: mean of dataset
    :param std: standard deviation of dataset
    :param d_train: features used for training
    :param d_predict: features used in prediction
    :return: normalized batch: tensor(#batch_size,#seq_len,#features*#stations)
    """
    while True:
        x, y = next(generator)
        yield normalize(x, mean, std, d_train), normalize(y, mean, std, d_predict)
