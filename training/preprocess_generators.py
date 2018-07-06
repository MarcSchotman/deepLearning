import numpy as np


def mean_day_night(batch):
    y_filtered = np.zeros((batch.shape[0], int(batch.shape[1] / 12)))
    for i in range(0, y_filtered.shape[1], 2):
        mean_night = (np.mean(batch[:, i * 12:i * 12 + 6], axis=1) + np.mean(batch[:, i * 12 + 18:], axis=1)) / 2
        mean_day = np.mean(batch[:, i * 12 + 6:i * 12 + 18], axis=1)
        y_filtered[:, i] = mean_day
        y_filtered[:, i + 1] = mean_night
    return y_filtered


def mean_day_night_generator(generator):
    """
    Replaces the hourly measurements with the mean at day and night time.
    :param generator:
    :return:
    """
    while True:
        x, y = next(generator)
        y_filtered = np.zeros((y.shape[0], int(y.shape[1] / 12), 1))
        for i in range(0, y_filtered.shape[1], 2):
            mean_night = (np.mean(y[:, i * 12:i * 12 + 6], axis=1) + np.mean(y[:, i * 12 + 18:], axis=1)) / 2
            mean_day = np.mean(y[:, i * 12 + 6:i * 12 + 18], axis=1)
            y_filtered[:, i] = mean_day
            y_filtered[:, i + 1] = mean_night
        yield x, y_filtered


def mean_hour_generator(generator,step=6):
    while True:
        x, y = next(generator)
        y_filtered = mean_hour(y,step)
        yield x, y_filtered


def mean_hour(batch, step=6):
    y_filtered = np.zeros((batch.shape[0], int(batch.shape[1] / step), batch.shape[2]))
    for i in range(0, batch.shape[1], step):
        mean_step = np.mean(batch[:, i:i + step], 1)
        y_filtered[:, int(i / step)] = mean_step
    return y_filtered


