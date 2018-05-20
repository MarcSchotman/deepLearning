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


def basic_lstm(batch_size=8, n_features=1, n_stations=21):
    """
    Creates a model with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: model
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=7, activation="relu")(input)
    dense2 = Dense(units=7, activation="relu")(dense1)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=3, activation="relu")(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

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
