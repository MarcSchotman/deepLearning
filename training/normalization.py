import numpy as np

_MISSING_VALUE = 999.9


def estimate_stats(generator, n_batches):
    """
    Estimates mean and stddev of dataset excluding missing data.
    :param generator: generator that loads dataset batchwise
    :param n_batches: number of batches
    :return: (mean,stddev)
    """
    mean_sum = 0
    std_sum = 0

    for i in range(n_batches):
        x, _ = next(generator)
        valid_idx = (x != _MISSING_VALUE)
        mean_sum += np.mean(x[valid_idx], axis=0)
        std_sum += np.std(x[valid_idx], axis=0)

    mean_est = mean_sum / n_batches
    std_est = std_sum / n_batches

    return mean_est, std_est


def normalize(batch, mean, std):
    """
    Normalize batch by taking into account missing values.
    :param batch_normed: tensor(#batch_size,#seq_len,#features*#stations)
    :param mean: mean of dataset
    :param std: standard deviation dataset
    :return: normalized batch: tensor(#batch_size,#seq_len,#features*#stations)
    """
    batch_normed = batch.copy()
    missing_idx = (batch_normed == _MISSING_VALUE)
    valid_idx = (batch_normed != _MISSING_VALUE)
    batch_normed[valid_idx] -= mean
    batch_normed[valid_idx] /= std
    batch_normed[missing_idx] = 0

    return batch_normed


def normalize_generator(generator, mean, std):
    """
    Generator to normalize batchwise before feeding it to the network.
    :param generator: generator that loads dataset batchwise
    :param mean: mean of dataset
    :param std: standard deviation of dataset
    :return: normalized batch: tensor(#batch_size,#seq_len,#features*#stations)
    """
    while True:
        x, y = next(generator)
        yield normalize(x, mean, std), normalize(y, mean, std)
