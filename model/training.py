from model.meijer import meijer_net
from model.preprocessing import load_data

model = meijer_net()
batch_size = 8
n_samples = 100
train_generator = load_data(data_dir='../RADIUS100KM/',
                            years=(2008, 2016),
                            batch_size=batch_size)

valid_generator = load_data(data_dir='../RADIUS100KM/',
                            years=(2017, 2018),
                            batch_size=batch_size)

model.compile(optimizer='Adam', loss='mean_squared_error')
model.fit_generator(generator=train_generator,
                    steps_per_epoch=int(n_samples / batch_size),
                    epochs=10,
                    validation_data=valid_generator,
                    validation_steps=100,
                    shuffle=True
                    )
