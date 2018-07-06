from pathlib import Path

from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, History, TerminateOnNaN, LearningRateScheduler, \
    ReduceLROnPlateau, CSVLogger


class Training:
    def __init__(self,
                 model,
                 out_file,
                 batch_size,
                 train_gen,
                 n_samples,
                 patience_early_stop=3,
                 patience_lr_reduce=2,
                 log_dir='./logs',
                 stop_on_nan=True,
                 lr_schedule=None,
                 lr_reduce=-1,
                 log_csv=True,
                 initial_epoch=0,
                 epochs=100,
                 callbacks=None, valid_gen=None):
        self.valid_gen = valid_gen
        self.train_gen = train_gen
        self.n_samples = n_samples
        self.model = model
        self.patience_lr_reduce = patience_lr_reduce
        self.initial_epoch = initial_epoch
        self.epochs = epochs
        self.batch_size = batch_size
        self.callbacks = []
        if patience_early_stop > -1:
            early_stop = EarlyStopping(monitor='val_loss', min_delta=0.001, patience=patience_early_stop, mode='min',
                                       verbose=1)
            self.callbacks.append(early_stop)
        if out_file is not None:
            checkpoint = ModelCheckpoint(log_dir + out_file, monitor='loss', verbose=2, save_best_only=True,
                                         mode='min', save_weights_only=False,
                                         period=1)
            self.callbacks.append(checkpoint)
        if log_dir is not None:
            tensorboard = TensorBoard(batch_size=batch_size, log_dir=log_dir, write_images=True,
                                      histogram_freq=0)
            self.callbacks.append(tensorboard)

        if stop_on_nan:
            stop_nan = TerminateOnNaN()
            self.callbacks.append(stop_nan)

        if lr_schedule is not None:
            schedule = LearningRateScheduler(schedule=lr_schedule)
            self.callbacks.append(schedule)

        if lr_reduce > -1:
            reducer = ReduceLROnPlateau(monitor='loss', factor=lr_reduce, patience=patience_lr_reduce, min_lr=0.00001)
            self.callbacks.append(reducer)

        if log_csv:
            log_file_name = log_dir + '/log.csv'
            append = Path(log_file_name).is_file() and initial_epoch > 0
            csv_logger = CSVLogger(log_file_name, append=append)
            self.callbacks.append(csv_logger)
        if callbacks is not None:
            self.callbacks.extend(callbacks)
        history = History()
        self.callbacks.append(history)

    def start(self):

        history = self.model.fit_generator(
            generator=self.train_gen,
            steps_per_epoch=(self.n_samples / self.batch_size),
            epochs=self.epochs,
            initial_epoch=self.initial_epoch,
            verbose=1,
            validation_data=self.valid_gen,
            validation_steps=100,
            callbacks=self.callbacks)

        return history.history

    @property
    def summary(self):

        summary = {'batch_size': self.batch_size,
                   'n_samples': self.n_samples,
                   'initial_epoch': self.initial_epoch,
                   'epochs': self.epochs,
                   'architecture': self.model.get_config(),
                   'weights': self.model.count_params()}
        return summary
