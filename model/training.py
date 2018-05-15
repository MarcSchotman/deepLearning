from model.meijer import meijer_net
from model.batch_generator import generate_batch


def train():
    model = meijer_net(n_stations=21)
    batch_size = 8
    n_samples = 100
    train_generator = generate_batch(data_dir='../data/',
                                     filenames=['2017'],
                                     batch_size=batch_size,
                                     station_id_pred='062090-99999')

    valid_generator = generate_batch(data_dir='../data/',
                                     filenames=['2017'],
                                     batch_size=batch_size,
                                     station_id_pred='062090-99999')

    model.compile(optimizer='Adam', loss='mean_squared_error')
    model.fit_generator(generator=train_generator,
                        steps_per_epoch=int(n_samples / batch_size),
                        epochs=10,
                        #validation_data=valid_generator,
                        validation_steps=100,
                        shuffle=True
                        )


if __name__ == "__main__":

    train()
