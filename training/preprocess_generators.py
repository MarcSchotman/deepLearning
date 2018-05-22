import numpy as np


def _mean_day_night(generator):
    """
    Replaces the hourly measurements with the mean at day and night time.
    :param generator:
    :return:
    """
    while True:
        x, y = next(generator)
        y_filtered = np.zeros((y.shape[0], int(y.shape[1] / 12)))
        for i in range(0, y_filtered.shape[1], 2):
            mean_night = (np.mean(y[:, i * 12:i * 12 + 6], axis=1) + np.mean(y[:, i * 12 + 18:], axis=1)) / 2
            mean_day = np.mean(y[:, i * 12 + 6:i * 12 + 18], axis=1)
            y_filtered[:, i] = mean_day
            y_filtered[:, i+1] = mean_night
        yield x, y_filtered


preprocess_generators = {
    'mean_day_night': _mean_day_night
}
