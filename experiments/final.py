from training.models import create_model
from training.train import train, MASK_VALUE

batch_size = 8
n_stations = 41
radius = 1000
t_train_h = 7 * 24
t_pred_d = 3
t_pred_resolution_h = 1
filenames_train = ['2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008']
filenames_valid = ['2016']
features_train = ['air_temperature']
features_predict = ['air_temperature']

"""
Experiment I: Final
"""
n_dense_pres = [1, 2, 3]
n_node = 1.0
act = 'relu'
n_memory = 2
n_dense_poss = [1, 2, 3]
memory_unit = 'lstm'
reg = None
for i in range(3):
    n_dense_pos = n_dense_poss[i]
    n_dense_pre = n_dense_pres[i]
    model = create_model(batch_size=batch_size,
                         t_train=t_train_h,
                         t_pred=int(t_pred_d * 24 / t_pred_resolution_h),
                         n_features_train=len(features_train),
                         n_stations=n_stations,
                         memory_unit=memory_unit,
                         width=n_dense_pre,
                         n_layers_memory=n_memory,
                         n_layers_preprocessing=n_dense_pre,
                         n_layers_postprocessing=n_dense_pos,
                         n_features_pred=len(features_predict),
                         activation=act,
                         mask_value=MASK_VALUE,
                         regularization=None)

    # '{layer_pre}x{n_nodes}*{act}->[{memory}]{n_lstm}->{layer_pos}{n_nodes}*{act}'
    log_dir = 'out/{}-{}-{}-{}{}-{}-{}-{}'.format(n_dense_pre, int(n_node * 10), act, memory_unit, n_memory,
                                                  n_dense_pos, int(n_stations / n_dense_pre), act)

    train(radius=radius,
          batch_size=batch_size,
          log_dir=log_dir,
          t_train_h=t_train_h,
          t_pred_d=t_pred_d,
          t_pred_resolution_h=t_pred_resolution_h,
          model_name=model,
          filenames_train=filenames_train,
          filenames_valid=filenames_valid,
          features_train=features_train,
          features_predict=features_predict,
          )
