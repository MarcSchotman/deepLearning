import pickle
import random

import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

from training.batch_generator import generate_batch
from training.normalization import normalize
from training.preprocess_generators import mean_day_night
from training.train import ENTRIES_PER_FILE, position
from training.utils import find_closest_station

model_file = '../out/basic_lstm/training.h5'
model = load_model(model_file)
batch_size = 8
data_dir = '../data/RADIUS200KM_PROCESSED/'
filenames_predict = ['2016']

file_cont = pickle.load(open(data_dir + random.choice(filenames_predict) + '.pickle', 'rb'))
station_id_pred, distance = find_closest_station(file_cont, position)
print("Desired location: {}, found closest station to be {} at distance {}".format(position, station_id_pred, distance))

generator = generate_batch(data_dir=data_dir,
                           filenames=filenames_predict,
                           batch_size=batch_size,
                           batches_per_file=int(ENTRIES_PER_FILE / 7 * 24),
                           station_id_pred=station_id_pred,
                           seq_len_pred=3 * 24,
                           seq_len_train=7 * 24)

mean, std = 5.817838704067266, 3.340678021019071
while True:
    x, y = next(generator)
    y_normalized = normalize(y, mean, std)
    y_true_normed = mean_day_night(y_normalized)
    y_true = (y_true_normed+mean)*std
    x_normalized = normalize(x, mean, std)
    x_cleaned = (x_normalized+mean)*std
    y_predicted_normed = model.predict(x)
    y_predicted = (y_predicted_normed + mean) * std
    for i_batch in range(batch_size):
        plt.figure()
        plt.plot(np.arange(0, 24*7), x_cleaned[i_batch, :, list(file_cont.keys()).index(station_id_pred)], 'gx--')
        plt.title("Past Temperature")
        plt.xlabel('Hour')
        plt.ylabel('Temperature')
        plt.figure()
        plt.plot(np.arange(0, 3 * 2), y_predicted[i_batch, :], 'bx--')
        plt.plot(np.arange(0, 3 * 2), y_true[i_batch, :], 'rx--')
        plt.xticks(np.arange(0, 3 * 2),['Night 1', 'Day 1', 'Night 2', 'Day 2', 'Night 3', 'Day 3'])
        plt.xlabel('Mean Night/Mean Day')
        plt.ylabel('Temperature')
        plt.legend(['Predicted Temperature', 'True Temperature'])
        plt.title('Future Temperature')
        plt.show()
