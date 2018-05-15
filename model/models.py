from keras import Input, Model
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, np


def meijer_net(seq_len_train=7, batch_size=8, n_features=1, n_stations=21, seq_len_pred=7):
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))
    conv1 = Conv1D(filters=1, kernel_size=2)(input)
    pool1 = MaxPooling1D()(conv1)
    dense1 = Dense(units=1, activation="elu")(pool1)
    # z = Lambda(append)(dense1)
    lstm = LSTM(units=7, stateful=True)(dense1)
    dense2 = Dense(units=1, activation="tanh")(lstm)
    dense3 = Dense(units=seq_len_pred, activation="linear")(dense2)
    model = Model(input, dense3)
    return model


def basic_lstm(seq_len_train=7, batch_size=8, n_features=1, n_stations=21, seq_len_pred=7):
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    dense1 = Dense(units=1, activation="elu")(input)
    dense2 = Dense(units=1, activation="elu")(dense1)
    lstm = LSTM(units=7, stateful=True)(dense2)
    dense2 = Dense(units=1, activation="tanh")(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense2)

    model = Model(input, out)
    return model


if __name__ == '__main__':
    monday_til_saturday = np.array([
        [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]],
        [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]],
        [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
    ])
    sunday = np.array([7,
                       7,
                       7,
                       ])
    model = meijer_net()
    model.compile(optimizer='Adam', loss='mean_squared_error')
    model.fit(x=monday_til_saturday, y=sunday, epochs=1, batch_size=3)
    prediction = model.predict(monday_til_saturday, batch_size=3, verbose=2)
    print(prediction)

models = {'meijer': meijer_net,
          'basic_lstm': basic_lstm}
