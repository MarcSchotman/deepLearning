import argparse
import pickle
import random
import sys

#from downloadData.functions.file_utils import create_dirs, save_file

sys.path.extend(['../'])

from training.normalization import estimate_stats, normalize_generator
from training.preprocess_generators import preprocess_generators
from training.utils import find_closest_station

from pprint import pprint

from training.Training import Training
from training.batch_generator import generate_batch
from training.models import models

"""
Script to start a training. 

It will create a directory in out/log_dir and save 
the trained training [training.h5], a summary of the training/training configuration [summary.txt]
and a summary of the training (loss per epoch) [log.csv].

It will also create a tensorboard logfile that enables visualization of the training graph
and training procedure with tensorboard. To visualize type:
 'python -m tensorboard.main --logdir=<Path-to-log_dir>'

Run this script from terminal with :
 'python train.py --model_name X --data_dir X --batch_size X --n_samples X --log_dir X/X'
"""
batch_size = 8
n_samples = None
log_dir = '../out/basic_lstm/'
data_dir = '../data/RADIUS100KM_PROCESSED/'
model_name = 'basic_gru'
station_id_pred = None
filenames_train = ['2015', '2016']
filenames_valid = ['2017']

ENTRIES_PER_FILE = 365 * 24
position = (39.7392, -104.99903)  # lat,lon

if __name__ == '__main__':
    """
    Overwrite parameters when run from command line
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--model_name', help='Name of the training to train: ' + str([str(k) for k in models.keys()]),
                           default=model_name)
    argparser.add_argument('--log_dir', help='Path to store training output', default=log_dir)
    argparser.add_argument('--data_dir', help='Path to read data files', default=data_dir)
    argparser.add_argument('--batch_size', help='Size of one Batch', default=batch_size)
    argparser.add_argument('--n_samples', help='Amount of samples to train', default=n_samples)
    args = argparser.parse_args()

    batch_size = args.batch_size
    log_dir = args.log_dir
    data_dir = args.data_dir
    model_name = args.model_name
    n_samples = args.n_samples

    if n_samples is None:
        n_samples = int(len(filenames_train) * ENTRIES_PER_FILE / 7 * 24)

    if not log_dir.endswith('/'):
        log_dir += '/'
    if not data_dir.endswith('/'):
        data_dir += '/'

    """
    Find station to predict for
    """
    content = pickle.load(open(data_dir + random.choice(filenames_train) + '.pickle', 'rb'))
    n_stations = len(list(content.keys()))
    station_id_pred, distance = find_closest_station(content, position)
    print("Desired location: {}, found closest station to be {} at distance {}".format(position, station_id_pred, distance))

    """
    Create Model
    """
    model = models[model_name](n_stations=n_stations, batch_size=batch_size)
    print('Training training: ', model_name)
    print('Storing files at: ', log_dir)
    print('Reading data from: ', data_dir)

    create_dirs([log_dir])

    """
    Create dataset generators
    """

    train_generator = generate_batch(data_dir=data_dir,
                                     filenames=filenames_train,
                                     batch_size=batch_size,
                                     batches_per_file=int(ENTRIES_PER_FILE / 7 * 24),
                                     station_id_pred=station_id_pred,
                                     seq_len_pred=3 * 24,
                                     seq_len_train=7 * 24)

    valid_generator = generate_batch(data_dir=data_dir,
                                     filenames=filenames_valid,
                                     batch_size=batch_size,
                                     batches_per_file=int(ENTRIES_PER_FILE / 7 * 24),
                                     station_id_pred=station_id_pred,
                                     seq_len_pred=3 * 24,
                                     seq_len_train=7 * 24)

    # We estimate mean and stddev from the trainingset to normalize our data
    mean, std = estimate_stats(train_generator, int(n_samples / batch_size))
    #mean, std = 5.817838704067266 , 3.340678021019071
    # We feed the train generators through normalize generators to normalize each batch before
    # feeding it in the network. This also gets rid of missing values
    train_generator = normalize_generator(train_generator, mean, std)
    valid_generator = normalize_generator(valid_generator, mean, std)

    # For now we predict only a mean temperature for day and night so we feed the generators
    # through preprocessors
    train_generator = preprocess_generators['mean_day_night'](train_generator)
    valid_generator = preprocess_generators['mean_day_night'](valid_generator)

    print("Dataset statistics: {} +- {}".format(mean, std))
    print("Number of samples: ", n_samples)

    """
    Configure Training
    """
    model.compile(optimizer='Adam', loss='mean_squared_error')
    training = Training(model=model,
                        out_file='training.h5',
                        batch_size=batch_size,
                        train_gen=train_generator,
                        valid_gen=valid_generator,
                        n_samples=n_samples,
                        log_dir=log_dir)
    pprint(training.summary)
    save_file(training.summary, name='summary.txt', path=log_dir)

    """
    Start Training
    """
    training.start()
