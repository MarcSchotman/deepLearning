import numpy as np

import matplotlib.pyplot as plt

from training.batch_generator import generate_batch
from training.normalization import estimate_stats, normalize

batch_size = 8
data_dir = '../data/RADIUS70KM_PROCESSED/'
model_name = 'basic_lstm'
station_id_pred = None
n_stations = 5
filenames_train = ['2017']
n_samples = 8
ENTRIES_PER_FILE = 365 * 24

gen = generate_batch(data_dir=data_dir,
                     filenames=filenames_train,
                     batch_size=batch_size,
                     station_id_pred=station_id_pred,
                     seq_len_pred=3 * 24,
                     seq_len_train=7 * 24)

# We estimate mean and stddev from the trainingset to normalize our data
mean, std = estimate_stats(gen, int(n_samples / batch_size))
print("Dataset statistics: {} +- {}".format(mean, std))

n_batches = int(n_samples / batch_size)
normalized_data = np.zeros((n_samples, 7 * 24, (n_stations-1)))
data = np.zeros((n_samples, 7 * 24, (n_stations-1)))
for i in range(n_batches):
    x, _ = next(gen)
    x_normed = normalize(x.copy(), mean, std)
    normalized_data[i:i + batch_size] = x_normed
    data[i:i + batch_size] = x

data_cleaned = data.copy()
data_cleaned[data_cleaned == 999.9] = 0
plt.plot(np.arange(0, data_cleaned.shape[1]), data_cleaned[0, :, 0], 'x--')
plt.title('Data')
plt.figure()
plt.plot(np.arange(0, 7 * 24), normalized_data[0, :, 0], 'x--')
plt.title('Normalized Data')

plt.show()
