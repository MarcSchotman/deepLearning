import argparse
import pickle
import random
import sys

sys.path.extend(['../'])
from downloadData.functions.file_utils import create_dirs, save_file

from training.normalization import estimate_stats, normalize_generator
from training.preprocess_generators import preprocess_generators
from training.utils import find_closest_station

from pprint import pprint

from training.Training import Training
from training.batch_generator import generate_batch
from training.models import models


def train(batch_size=4,
          n_samples=None,
          log_dir='../out/m2m_gru/',
          data_dir='../data/RADIUS500KM/data/RADIUS500KM_PROCESSED/',
          t_train_h=7 * 24,
          t_pred_d=3,
          t_pred_resolution_h=1,
          model_name='m2m_gru',
          filenames_train=['2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008'],
          filenames_valid=['2017'],
          mean=None,
          std=None,
          ENTRIES_PER_FILE=365 * 24,
          position=(39.7392, -104.99903)):
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
    t_pred = int(t_pred_d * 24 / t_pred_resolution_h)

    if n_samples is None:
        n_samples = int(len(filenames_train) * ENTRIES_PER_FILE / t_train_h)

    if not log_dir.endswith('/'):
        log_dir += '/'
    if not data_dir.endswith('/'):
        data_dir += '/'

    """
    Find station to predict for
    """
    content = pickle.load(open(data_dir + random.choice(filenames_train) + '.pickle', 'rb'))
    n_stations = len(list(content.keys()))
    print("Number of stations: {}".format(n_stations))
    station_id_pred, distance = find_closest_station(content, position)
    print("Desired location: {}, found closest station to be {} at distance {}".format(position, station_id_pred,
                                                                                       distance))

    """
    Create Model
    """
    model = models[model_name](n_stations=n_stations, batch_size=batch_size, seq_len_pred=t_pred,
                               seq_len_train=t_train_h)
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
                                     station_id_pred=station_id_pred,
                                     seq_len_pred=t_pred_d * 24,
                                     seq_len_train=t_train_h)

    valid_generator = generate_batch(data_dir=data_dir,
                                     filenames=filenames_valid,
                                     batch_size=batch_size,
                                     station_id_pred=station_id_pred,
                                     seq_len_pred=t_pred_d * 24,
                                     seq_len_train=t_train_h)

    # We estimate mean and stddev from the trainingset to normalize our data
    if mean is None or std is None:
        mean, std = estimate_stats(train_generator, int(n_samples / batch_size))

    # We feed the train generators through normalize generators to normalize each batch before
    # feeding it in the network. This also gets rid of missing values
    train_generator = normalize_generator(train_generator, mean, std)
    valid_generator = normalize_generator(valid_generator, mean, std)

    # For now we predict only a mean temperature for day and night so we feed the generators
    # through preprocessors
    train_generator = preprocess_generators['mean_hour'](train_generator, step=t_pred_resolution_h)
    valid_generator = preprocess_generators['mean_hour'](valid_generator, step=t_pred_resolution_h)

    print("Dataset statistics: {} +- {}".format(mean, std))
    print("Number of samples: ", n_samples)

    """
    Configure Training
    """
    model.compile(optimizer='Adam', loss='mean_squared_error')
    training = Training(model=model,
                        out_file='model.h5',
                        batch_size=batch_size,
                        train_gen=train_generator,
                        valid_gen=valid_generator,
                        n_samples=n_samples,
                        log_dir=log_dir)
    pprint(training.summary)
    summary = training.summary
    summary['mean'] = mean
    summary['std'] = std
    summary['t_train_h'] = t_train_h
    summary['t_pred'] = t_pred
    summary['t_pred_resolution_h'] = t_pred_resolution_h
    save_file(summary, name='summary.txt', path=log_dir)

    """
    Start Training
    """
    training.start()


if __name__ == '__main__':
    """
    Overwrite parameters when run from command line
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--model_name',
                           help='Name of the training to train: ' + str([str(k) for k in models.keys()]),
                           default='m2m_lstm')
    argparser.add_argument('--log_dir', help='Path to store training output', default='out/temp/')
    argparser.add_argument('--data_dir', help='Path to read data files', default='../data/RADIUS500KM_PROCESSED')
    argparser.add_argument('--batch_size', help='Size of one Batch', default=8)
    argparser.add_argument('--n_samples', help='Amount of samples to train', default=None)
    args = argparser.parse_args()

    train(batch_size=args.batch_size,
          log_dir=args.log_dir,
          data_dir=args.data_dir,
          model_name=args.model_name,
          n_samples=args.n_samples)
