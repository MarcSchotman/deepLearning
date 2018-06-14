import argparse
import pickle
import random
import sys

sys.path.extend(['../', './'])

# from downloadData.functions.file_utils import create_dirs, save_file
from training.models import meijer_net, basic_lstm, basic_gru, basic_lstm_dropout30, basic_lstm_dropout50, \
    basic_lstm_l1, basic_lstm_l2, basic_lstm_l1_act, basic_lstm_l2_act, basic_lstm_smaller, m2m_lstm, m2m_lstm_norm, \
    m2m_gru
from training.preprocess_generators import mean_day_night_generator, mean_hour_generator

from downloadData.functions.file_utils import create_dirs, save_file

from training.normalization import estimate_stats, normalize_generator
from training.utils import find_closest_station

from pprint import pprint

from training.Training import Training
from training.batch_generator import generate_batch

models = {'meijer': meijer_net,
          'basic_lstm': basic_lstm,
          'basic_gru': basic_gru,
          'lstm_drop30': basic_lstm_dropout30,
          'lstm_drop50': basic_lstm_dropout50,
          'lstm_kernel_l1': basic_lstm_l1,
          'lstm_kernel_l2': basic_lstm_l2,
          'lstm_kernel_actl1': basic_lstm_l1_act,
          'lstm_kernel_actl2': basic_lstm_l2_act,
          'lstm_small': basic_lstm_smaller,
          'm2m_lstm': m2m_lstm,
          'm2m_lstm_norm': m2m_lstm_norm,
          'm2m_gru': m2m_gru}

preprocess_generators = {
    'mean_day_night': mean_day_night_generator,
    'mean_hour': mean_hour_generator
}

# default values
# DATA_DIR = '../data/RADIUS500KM_PROCESSED/'
RADIUS = 100
LOG_DIR = '../out/m2m_lstm/'
BATCH_SIZE = 4
MODEL_NAME = 'm2m_lstm'
POSITION = (39.7392, -104.99903)
FEATURES_TRAIN = ['air_temperature']
FEATURES_PREDICT = ['air_temperature']
FILENAMES_TRAIN = ['2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008']
FILENAMES_VALID = ['2017']
T_TRAIN_H = 7 * 24
T_PRED_D = 3
MASK_VALUE = 999


def train(batch_size=BATCH_SIZE,
          n_samples=None,
          radius=RADIUS,
          t_train_h=T_TRAIN_H,
          t_pred_d=T_PRED_D,
          t_pred_resolution_h=1,
          model_name=MODEL_NAME,
          filenames_train=FILENAMES_TRAIN,
          filenames_valid=FILENAMES_VALID,
          mean=None,
          std=None,
          file_len=365 * 24,
          position=POSITION,
          features_train=FEATURES_TRAIN,
          features_predict=FEATURES_PREDICT,
          mask_value=MASK_VALUE):
    """
    Script to start a training.

    It will create a directory in out/log_dir and save
    the trained training [model.h5], a summary of the training/training configuration [summary.txt/summary.pkl],
    and a log of the training (loss per epoch) [log.csv].

    It will also create a tensorboard logfile that enables visualization of the training graph
    and training procedure with tensorboard. To visualize type:
     'python -m tensorboard.main --logdir=<Path-to-log_dir>'

    Run this script from terminal with :
     'python train.py --model_name X --data_dir X --batch_size X --n_samples X --log_dir X/X'
    """
    
    data_dir = '../data/RADIUS' + str(radius) + 'KM_PROCESSED/'
    log_dir = '../out/' + model_name + '_'.join(features_train) + '/' + str(radius) + '/'
    
    
    t_pred = int(t_pred_d * 24 / t_pred_resolution_h)

    if n_samples is None:
        n_samples = int(len(filenames_train) * file_len / t_train_h)

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
                               seq_len_train=t_train_h, n_features=len(features_train),
                               n_features_pred=len(features_predict), mask_value=mask_value, padding=t_pred_d * 24)
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
                                     t_pred=t_pred_d * 24,
                                     t_train=t_train_h,
                                     features_train=features_train,
                                     features_pred=features_predict,
                                     padding=t_pred_d * 24,
                                     pad_value=mask_value
                                     )

    valid_generator = generate_batch(data_dir=data_dir,
                                     filenames=filenames_valid,
                                     batch_size=batch_size,
                                     station_id_pred=station_id_pred,
                                     t_pred=t_pred_d * 24,
                                     t_train=t_train_h,
                                     features_train=features_train,
                                     features_pred=features_predict,
                                     padding=t_pred_d * 24,
                                     pad_value=mask_value,
                                     )

    # We estimate mean and stddev from the trainingset to normalize our data
    if mean is None or std is None:
        mean, std = estimate_stats(train_generator, int(n_samples / batch_size),
                                   len(features_train),
                                   mask_value=mask_value)

    # We feed the train generators through normalize generators to normalize each batch before
    # feeding it in the network. This also gets rid of missing values
    train_generator = normalize_generator(train_generator, mean, std, len(features_train), len(features_predict),
                                          mask_value=mask_value)
    valid_generator = normalize_generator(valid_generator, mean, std, len(features_train), len(features_predict),
                                          mask_value=mask_value)

    # For now we predict only a mean temperature for day and night so we feed the generators
    # through preprocessors
    train_generator = preprocess_generators['mean_hour'](train_generator, step=t_pred_resolution_h)
    valid_generator = preprocess_generators['mean_hour'](valid_generator, step=t_pred_resolution_h)

    print("Dataset statistics: {} +- {}".format(mean, std))
    print("Number of samples: ", n_samples)
    save_file([mean[0], std[0], n_samples], name='data_stat.txt', path=log_dir)
    
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
    """
    Store training details
    """
    summary = training.summary
    summary['model_name'] = model_name
    summary['files_training'] = filenames_train
    summary['files_valid'] = filenames_valid
    summary['station_to_predict'] = station_id_pred
    summary['mean'] = mean
    summary['std'] = std
    summary['t_train_h'] = t_train_h
    summary['t_pred'] = t_pred
    summary['t_pred_resolution_h'] = t_pred_resolution_h
    summary['features_train'] = features_train
    summary['features_pred'] = features_predict
    pprint(summary)

    save_file(summary, name='summary.txt', path=log_dir)
    save_file(summary, name='summary.pkl', path=log_dir)

    """
    Oppaa!
    """
    training.start()


if __name__ == '__main__':
    """
    Overwrite parameters when run from command line
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--model_name',
                           help='Name of the model to train. Available:\n ' + str([str(k) for k in models.keys()]),
                           default=MODEL_NAME)
    argparser.add_argument('--log_dir', help='Path to store training output', default=LOG_DIR)
    argparser.add_argument('--data_dir', help='Path to read data files', default=RADIUS)
    argparser.add_argument('--batch_size', help='Size of one Batch', default=BATCH_SIZE)
    argparser.add_argument('--n_samples', help='Amount of samples to train', default=None)
    args = argparser.parse_args()
    train()
   # train(batch_size=args.batch_size,
   #       log_dir=args.log_dir,
   #       data_dir=args.data_dir,
   #       model_name=args.model_name,
   #       n_samples=args.n_samples)
