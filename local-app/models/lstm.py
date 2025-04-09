import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense



def lstm_train(X_train, X_test, y_train, y_test, dataset, dt, look_back=3):
    data = dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)
    train_size = int(len(data_scaled) * 0.80)
    train_data, test_data = data_scaled[:train_size], data_scaled[train_size:]

    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset) - look_back -1):
            a = dataset[i:(i + look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)
    X_train, Y_train = create_dataset(train_data, look_back)
    X_test, Y_test = create_dataset(test_data, look_back)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # LSTM model
    model = Sequential()
    model.add(LSTM(units=25, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=25))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, Y_train, epochs=40, batch_size=900, verbose=0)
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # Inverse transform the predictions
    train_predict = scaler.inverse_transform(np.concatenate((train_predict, np.zeros((len(train_predict), len(data.columns) - 1))), axis=1))[:, 0]
    Y_train = scaler.inverse_transform(np.concatenate((Y_train.reshape(-1, 1), np.zeros((len(Y_train), len(data.columns) - 1))), axis=1))[:, 0]
    test_predict = scaler.inverse_transform(np.concatenate((test_predict, np.zeros((len(test_predict), len(data.columns) - 1))), axis=1))[:, 0]
    Y_test = scaler.inverse_transform(np.concatenate((Y_test.reshape(-1, 1), np.zeros((len(Y_test), len(data.columns) - 1))), axis=1))[:, 0]


    tmp = pd.concat([dt[train_size + look_back + 1:][:len(test_predict)],
                    y_test[:len(test_predict)],
                    pd.Series(test_predict, index=y_test[:len(test_predict)].index, name='pred')],
                    axis=1).dropna()

    return tmp
