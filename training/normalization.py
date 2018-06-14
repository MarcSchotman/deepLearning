import numpy as np


def estimate_stats(generator, n_batches, d, mask_value=999):
    """
    Estimates mean and stddev of dataset excluding missing data.
    :param d: number of features
    :param mask_value: used for missing values, will not be considered
    :param generator: generator that loads dataset batchwise
    :param n_batches: number of batches
    :return: (mean,stddev)
    """
    mean_sum = np.zeros((d,), dtype=float)
    std_sum = np.zeros((d,), dtype=float)

    mean_est = np.zeros((d,), dtype=float)
    std_est = np.zeros((d,), dtype=float)

    for i in range(n_batches):
        x, _ = next(generator)
        # reshape
        batch_size, seq_len, features_stations = x.shape
        stations_len = int(features_stations / d)

        x = np.reshape(x, (batch_size, seq_len, stations_len, d))

        for index_feature in range(d):
            valid_idx = (x[:, :, :, index_feature] != mask_value)
            mean_sum[index_feature] += np.mean(x[valid_idx, index_feature], axis=0)
            std_sum[index_feature] += np.std(x[valid_idx, index_feature], axis=0)

            mean_est[index_feature] = mean_sum[index_feature] / n_batches
            std_est[index_feature] = std_sum[index_feature] / n_batches

    #       print(mean_est[0], mean_est[1])

    # print(mean_est[0], mean_est[1])
    return mean_est, std_est


def normalize(batch, mean, std, d, mask_value=999):
    """
    Normalize batch by taking into account missing values.
    :param mask_value: used for missing values, will not be considered
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
        missing_idx = (batch[:, :, :, index_feature] == mask_value)
        valid_idx = (batch[:, :, :, index_feature] != mask_value)

        batch[valid_idx] -= mean[index_feature]
        batch[valid_idx] /= std[index_feature]
        batch[missing_idx] = 0
    # reshape back to original
    batch = np.reshape(batch, (batch_size, seq_len, stations_len * d))
    return batch


def normalize_generator(generator, mean, std, d_train, d_predict, mask_value=999):
    """
    Generator to normalize batchwise before feeding it to the network.
    :param generator: generator that loads dataset batchwise
    :param mask_value: used for missing values, will not be considered
    :param mean: mean of dataset
    :param std: standard deviation of dataset
    :param d_train: features used for training
    :param d_predict: features used in prediction
    :return: normalized batch: tensor(#batch_size,#seq_len,#features*#stations)
    """
    while True:
        x, y = next(generator)
        yield normalize(x, mean, std, d_train, mask_value), normalize(y, mean, std, d_predict, mask_value)
