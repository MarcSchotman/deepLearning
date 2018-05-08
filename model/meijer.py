from keras import Input, Model
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, np


def append(input, digit):
    pass


def meijer_net():
    input = Input(shape=(7, 2), batch_shape=(3, 7, 2))
    conv1 = Conv1D(filters=1, kernel_size=2)(input)
    pool1 = MaxPooling1D()(conv1)
    dense1 = Dense(units=1, activation="elu")(pool1)
    # z = Lambda(append)(dense1)
    lstm = LSTM(units=7, stateful=True)(dense1)
    dense2 = Dense(units=1, activation="tanh")(lstm)
    dense3 = Dense(units=1, activation="linear")(dense2)
    model = Model(input, dense3)
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
