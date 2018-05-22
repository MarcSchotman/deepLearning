import argparse
import sys

from model.normalization import estimate_stats, normalize_generator

sys.path.extend('../')
from pprint import pprint

from file_utils import create_dirs, save_file
from model.Training import Training
from model.batch_generator import generate_batch
from model.models import basic_lstm, models


def train(model, batch_size: int, n_samples: int, log_dir: str, data_dir: str, seq_len_train=7*24):
    create_dirs([log_dir])
    filenames = ['2015', '2016', '2017']
    train_generator = generate_batch(data_dir=data_dir,
                                     filenames=filenames,
                                     batch_size=batch_size,
                                     batches_per_file=int(365*24/seq_len_train),
                                     station_id_pred=None,
                                     seq_len_pred=24,
                                     seq_len_train=seq_len_train)

    if n_samples is None:
        n_samples = len(filenames)*365*24/seq_len_train

    mean, std = estimate_stats(train_generator, int(n_samples / batch_size))

    print("Dataset statistics: {} +- {}".format(mean, std))
    print("Number of samples: ", n_samples)

    valid_generator = generate_batch(data_dir=data_dir,
                                     filenames=['2017'],
                                     batch_size=batch_size,
                                     station_id_pred='062090-99999')

    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])
    training = Training(model=model,
                        out_file='model.h5',
                        batch_size=batch_size,
                        train_gen=normalize_generator(train_generator, mean, std),
                        n_samples=n_samples,
                        log_dir=log_dir)
    pprint(training.summary)
    save_file(training.summary, name='summary.txt', path=log_dir)

    training.start()


if __name__ == "__main__":
    """
    Run from terminal with python train.py --model_name X --data_dir X --batch_size X --n_samples X --log_dir X/X
    """
    batch_size = 8
    n_samples = None
    log_dir = '../out/basic_lstm'
    data_dir = '../data/RADIUS70KM_PROCESSED'
    model_name = 'basic_lstm'

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--model_name', help='Name of the model to train: ' + str([str(k) for k in models.keys()]),
                           default=model_name)
    argparser.add_argument('--log_dir', help='Path to store training output', default=log_dir)
    argparser.add_argument('--data_dir', help='Path to read data files', default=data_dir)
    argparser.add_argument('--batch_size', help='Size of one Batch', default=batch_size)
    argparser.add_argument('--n_samples', help='Amount of samples to train', default=n_samples)
    args = argparser.parse_args()

    if not args.log_dir.endswith('/'):
        args.log_dir += '/'
    if not args.data_dir.endswith('/'):
        args.data_dir += '/'

    model = models[args.model_name](n_stations=5,seq_len_pred=24,seq_len_train=7*24)
    print('Training model: ', args.model_name)
    print('Storing files at: ', args.log_dir)
    print('Reading data from: ', args.data_dir)

    train(model,
          batch_size=args.batch_size,
          n_samples=args.n_samples,
          log_dir=args.log_dir,
          data_dir=args.data_dir)
