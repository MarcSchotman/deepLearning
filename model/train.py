import argparse
import sys

sys.path.extend('../')
from pprint import pprint

from file_utils import create_dirs, save_file
from model.Training import Training
from model.batch_generator import generate_batch
from model.models import basic_lstm, models


def train(model, batch_size: int, n_samples: int, log_dir: str, data_dir:str):

    create_dirs([log_dir])

    train_generator = generate_batch(data_dir=data_dir,
                                     filenames=['2017'],
                                     batch_size=batch_size,
                                     station_id_pred='062090-99999')

    valid_generator = generate_batch(data_dir=data_dir,
                                     filenames=['2017'],
                                     batch_size=batch_size,
                                     station_id_pred='062090-99999')

    model.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])
    training = Training(model=model,
                        out_file=log_dir + '/model.h5',
                        batch_size=batch_size,
                        train_gen=train_generator,
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
    n_samples = 55
    log_dir = '../out/basic_lstm'
    data_dir = '../data/'
    model_name = 'basic_lstm'

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--model_name', help='Name of the model to train: ' + str([str(k) for k in models.keys()]),default=model_name)
    argparser.add_argument('--log_dir', help='Path to store training output', default=log_dir)
    argparser.add_argument('--data_dir', help='Path to read data files', default=data_dir)
    argparser.add_argument('--batch_size', help='Size of one Batch', default=batch_size)
    argparser.add_argument('--n_samples', help='Amount of samples to train', default=n_samples)
    args = argparser.parse_args()

    if not args.log_dir.endswith('/'):
        args.log_dir += '/'
    if not args.data_dir.endswith('/'):
        args.data_dir += '/'

    model = models[args.model_name]()
    print('Training model: ', args.model_name)
    print('Storing files at: ', args.log_dir)
    print('Reading data from: ', args.data_dir)

    train(model,
          batch_size=args.batch_size,
          n_samples=args.n_samples,
          log_dir=args.log_dir,
          data_dir=args.data_dir)
