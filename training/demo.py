import pickle
import random
import sys
import os

import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model

# from training import train

sys.path.extend(['../','./'])

from training.batch_generator import generate_batch
from training.normalization import normalize
from training.preprocess_generators import mean_hour
from training.utils import find_closest_station

model_file = os.path.join('..', 'out', 'm2m_lstmair_temperature','1000','model.h5')
model = load_model('../model.h5')
batch_size = 4
data_dir = '../data/RADIUS1000KM_PROCESSED/'
filenames_predict = ['2017']
t_train_h = 7 * 24
t_pred_h = 3 * 24
t_pred_resolution = 1
t_pred = int(t_pred_h / t_pred_resolution)

# This was estimated on the training set
mean, std = [8.371623727535322], [10.89360715785454]
d = 1
position = (39.7392, -104.99903)

"""
Find closest station
"""
file_cont = pickle.load(open(data_dir + random.choice(filenames_predict) + '.pickle', 'rb'))
station_id_pred, distance = find_closest_station(file_cont, position)
print("Desired location: {}, found closest station to be {} at distance {}".format(position, station_id_pred, distance))

"""
Load test data
"""
generator = generate_batch(data_dir=data_dir,
                           filenames=filenames_predict,
                           batch_size=batch_size,
                           station_id_pred=station_id_pred,
                           t_pred=t_pred_h,
                           t_train=t_train_h,
                           padding=72,
                           features_train=['air_temperature'])
csfont = {'fontname': 'Century Gothic'}

"""
Predict and show
"""
while True:
    x, y = next(generator)
    y_normalized = normalize(y, mean, std, d)
    y_clean = y_normalized * std + mean
    y_true_mean = mean_hour(y_clean, t_pred_resolution)

    x_normalized = normalize(x, mean, std, d)
    x_cleaned = x_normalized * std + mean
    y_predicted_normed = model.predict(x_normalized)
    y_predicted = y_predicted_normed * std + mean
    for i_batch in range(batch_size):
        x_i_station = x_cleaned[i_batch, :, list(file_cont.keys()).index(station_id_pred)]
        y_true_i = y_clean[i_batch]
        y_pred_i = y_predicted[i_batch]
        y_max = np.maximum(np.max(y_true_i), np.max(x_i_station))
        y_min = np.minimum(np.min(y_true_i), np.min(x_i_station))
        y_max += 0.3 * y_max
        y_min -= 0.3 * y_min

        plt.figure()
        # plt.subplot(2, 1, 1)
        # plt.ylim((y_min, y_max))
        # plt.plot(np.arange(0, t_train_h), x_i_station, 'gx--')
        # plt.title("Past Temperature At Target Station - Truth")
        # plt.xlabel('Hour')
        # plt.ylabel('Temperature')
        # plt.subplot(3, 1, 2)
        # plt.ylim((y_min, y_max))
        # plt.plot(np.arange(0, t_pred_h), y_true_i, 'gx--')
        # plt.title("Future Temperature - Truth")
        # plt.xlabel('Hour')
        # plt.ylabel('Temperature')
        # plt.subplot(2, 1, 2)
        # plt.ylim((y_min, y_max))
        plt.plot(np.arange(0, t_pred), y_pred_i, 'bx--')
        plt.plot(np.arange(0, t_pred), y_true_mean[i_batch], 'gx--')
        #plt.xticks(np.arange(0, t_pred), np.arange(0, t_pred_h, t_pred_resolution),fontsize=16, **csfont)
        plt.xlabel('Hour'.format(t_pred_resolution), fontsize=16, **csfont)
        plt.ylabel('Temperature', fontsize=16, **csfont)
        plt.legend(['Predicted Temperature', 'True Temperature'],prop={'family': 'Century Gothic', 'size'   : 13}, )
        plt.title('Future Temperature - Training Goal', fontsize=16, **csfont)
        plt.show()
