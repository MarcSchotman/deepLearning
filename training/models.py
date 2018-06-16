from keras import Input, Model
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, np, GRU, Dropout, regularizers, Lambda, BatchNormalization, \
    Activation, Masking, LeakyReLU


def meijer_net(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
               seq_len_pred=6, n_features_pred=1):
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


def basic_lstm(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
               seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu")(input)
    dense2 = Dense(units=14, activation="elu")(dense1)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=6, activation="tanh")(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

    model = Model(input, out)
    return model


def basic_lstm_smaller(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                       seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense2 = Dense(units=14, activation="elu")(input)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    out = Dense(units=seq_len_pred, activation="linear")(lstm)

    model = Model(input, out)
    return model


def basic_lstm_dropout50(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                         seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu")(input)
    drop1 = Dropout(rate=0.5)(dense1)
    dense2 = Dense(units=14, activation="elu")(drop1)
    drop2 = Dropout(rate=0.5)(dense2)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(drop2)
    dense3 = Dense(units=6, activation="tanh")(lstm)
    drop2 = Dropout(rate=0.5)(dense3)
    out = Dense(units=seq_len_pred, activation="linear")(drop2)

    model = Model(input, out)
    return model


def basic_lstm_dropout30(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                         seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu")(input)
    drop1 = Dropout(rate=0.3)(dense1)
    dense2 = Dense(units=14, activation="elu")(drop1)
    drop2 = Dropout(rate=0.3)(dense2)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(drop2)
    dense3 = Dense(units=6, activation="tanh")(lstm)
    drop2 = Dropout(rate=0.3)(dense3)
    out = Dense(units=seq_len_pred, activation="linear")(drop2)

    model = Model(input, out)
    return model


def basic_lstm_l1(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                  seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu", kernel_regularizer=regularizers.l1(0.01))(input)
    dense2 = Dense(units=14, activation="elu", kernel_regularizer=regularizers.l1(0.01))(dense1)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=6, activation="tanh", kernel_regularizer=regularizers.l1(0.01))(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

    model = Model(input, out)
    return model


def basic_lstm_l2(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                  seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu", kernel_regularizer=regularizers.l2(0.01))(input)
    dense2 = Dense(units=14, activation="elu", kernel_regularizer=regularizers.l2(0.01))(dense1)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=6, activation="tanh", kernel_regularizer=regularizers.l2(0.01))(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

    model = Model(input, out)
    return model


def basic_lstm_l1_act(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                      seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu", activity_regularizer=regularizers.l1(0.01))(input)
    dense2 = Dense(units=14, activation="elu", activity_regularizer=regularizers.l1(0.01))(dense1)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=6, activation="tanh", activity_regularizer=regularizers.l1(0.01))(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

    model = Model(input, out)
    return model


def basic_lstm_l2_act(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                      seq_len_pred=6, n_features_pred=1):
    """
    Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
    7 days and we predict the mean temperature at day and at night for the following 7 days.
    :param batch_size: Size of one batch
    :param n_features: Number of features per station
    :param n_stations: Number of stations
    :param seq_len_pred: Sequence length to predict
    :return: training
    """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="elu", activity_regularizer=regularizers.l2(0.01))(input)
    dense2 = Dense(units=14, activation="elu", activity_regularizer=regularizers.l2(0.01))(dense1)
    # Lstm keeps track of time dependencies
    lstm = LSTM(units=1, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=6, activation="tanh", activity_regularizer=regularizers.l2(0.01))(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

    model = Model(input, out)
    return model


def basic_gru(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
              seq_len_pred=6, n_features_pred=1):
    """
        Creates a training with lstm. Inspired by the network of meijer. We input the hourly temperature for
        7 days and we predict the mean temperature at day and at night for the following 7 days.
        :param batch_size: Size of one batch
        :param n_features: Number of features per station
        :param n_stations: Number of stations
        :param seq_len_pred: Sequence length to predict
        :return: training
        """
    seq_len_train = 7 * 24
    seq_len_pred = 6
    input = Input(shape=(seq_len_train, n_features * n_stations),
                  batch_shape=(batch_size, seq_len_train, n_features * n_stations))

    # We have two dense units to preprocess the input. We use 7 units as the idea is that the network abstracts
    # from the high resolution to a per day representation.
    dense1 = Dense(units=14, activation="relu")(input)
    dense2 = Dense(units=14, activation="relu")(dense1)
    # Lstm keeps track of time dependencies
    lstm = GRU(units=3, batch_input_shape=(batch_size, seq_len_train, n_stations * n_features))(dense2)
    dense3 = Dense(units=6, activation="relu")(lstm)
    out = Dense(units=seq_len_pred, activation="linear")(dense3)

    model = Model(input, out)
    return model


def _dense_norm_relu(units, input):
    dense = Dense(units, use_bias=False)(input)
    norm = BatchNormalization()(dense)
    act = Activation('relu')(norm)
    return act


def m2m_lstm(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
             seq_len_pred=6, n_features_pred=1, mask_value=999, padding=0):
    input = Input(batch_shape=(batch_size, seq_len_train + padding, n_features * n_stations))
    mask = Masking(mask_value=mask_value)(input)
    dense1 = Dense(n_stations, activation="relu")(mask)
    dense2 = Dense(int(n_stations / 2), activation="relu")(dense1)

    dense3 = Dense(int(n_stations / 4), activation="relu")(dense2)
    dense4 = Dense(int(n_stations / 4), activation="relu")(dense3)
    lstm1 = LSTM(int(n_stations / 4), input_shape=(seq_len_train, n_stations * n_features), return_sequences=True)(
        dense4)
    shift = Lambda(lambda x: x[:, -seq_len_pred:, :])(lstm1)
    dense5 = Dense(int(n_stations / 4), activation="relu")(shift)
    dense6 = Dense(int(n_stations / 4), activation="relu")(dense5)
    out = Dense(units=n_features_pred, activation="linear")(dense6)
    return Model(input, out)


def m2m_gru(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
            seq_len_pred=6, n_features_pred=1):
    input = Input(batch_shape=(batch_size, seq_len_train, n_features * n_stations))
    dense1 = Dense(n_stations, activation="relu")(input)
    dense2 = Dense(int(n_stations / 2), activation="relu")(dense1)

    dense3 = Dense(int(n_stations / 4), activation="relu")(dense2)
    dense4 = Dense(int(n_stations / 4), activation="relu")(dense3)
    lstm1 = GRU(int(n_stations / 4), input_shape=(seq_len_train, n_stations * n_features), return_sequences=True)(
        dense4)
    shift = Lambda(lambda x: x[:, -seq_len_pred:, :])(lstm1)
    dense5 = Dense(int(n_stations / 4), activation="relu")(shift)
    dense6 = Dense(int(n_stations / 4), activation="relu")(dense5)
    out = Dense(units=n_features_pred, activation="linear")(dense6)
    return Model(input, out)


def m2m_lstm_norm(batch_size=8, n_features=1, n_stations=21, seq_len_train=7 * 24,
                  seq_len_pred=6, n_features_pred=1):
    input = Input(batch_shape=(batch_size, seq_len_train, n_features * n_stations))
    dense1 = _dense_norm_relu(n_stations, input)
    dense2 = _dense_norm_relu(int(n_stations / 2), dense1)
    dense3 = _dense_norm_relu(int(n_stations / 4), dense2)
    dense4 = _dense_norm_relu(int(n_stations / 4), dense3)

    lstm1 = LSTM(int(n_stations / 4), input_shape=(seq_len_train, n_stations * n_features), return_sequences=True)(
        dense4)

    shift = Lambda(lambda x: x[:, -seq_len_pred:, :])(lstm1)

    dense5 = _dense_norm_relu(int(n_stations / 4), shift)
    dense6 = _dense_norm_relu(int(n_stations / 4), dense5)

    out = Dense(units=n_features_pred, activation="linear")(dense6)
    return Model(input, out)


def create_preprocessing(netin, n_stations, activation, depth, width):
    conn = netin
    for i in range(1, depth + 1):
        conn = Dense(units=int(max(n_stations / i * width, 0)))(conn)
        if activation == 'leaky_relu':
            conn = LeakyReLU()(conn)
        else:
            conn = Activation(activation)(conn)
    return conn


def create_postprocessing(netin, activation, depth, width):
    conn = netin
    for i in range(depth):
        conn = Dense(int(width))(conn)
        if activation == 'leaky_relu':
            conn = LeakyReLU()(conn)
        else:
            conn = Activation(activation)(conn)
    return conn


def create_memory(netin, memory, depth, width):
    conn = netin
    for i in range(depth):
        conn = LSTM(width, return_sequences=True)(conn) if memory == 'lstm' else GRU(width,
                                                                                     return_sequences=True)(
            conn)
    return conn


def create_model(batch_size, t_train, n_features_train, n_stations, width, n_layers_preprocessing, activation,
                 n_layers_memory,
                 memory_unit, n_layers_postprocessing, t_pred, mask_value, n_features_pred):
    netin = Input(batch_shape=(batch_size, t_train + t_pred, n_features_train * n_stations))
    mask = Masking(mask_value=mask_value)(netin)

    preprocessing = create_preprocessing(mask, n_stations, activation, n_layers_preprocessing, width)
    memory_unit = create_memory(preprocessing, memory_unit, n_layers_memory, int(n_stations / n_layers_preprocessing))
    shift = Lambda(lambda x: x[:, -t_pred:, :])(memory_unit)
    postprocessing = create_postprocessing(shift, activation, n_layers_postprocessing,
                                           int(n_stations / n_layers_preprocessing))
    out = Dense(n_features_pred)(postprocessing)
    model = Model(netin, out)

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
