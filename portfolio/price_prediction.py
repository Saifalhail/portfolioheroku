import numpy as np
from numpy.core.fromnumeric import size
from numpy.lib.npyio import load
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
import os

def run(company):
    # file_name = csv_file if csv_file else 'tickertagGWCS.QA.csv'
    # company = "AAPL"
    
    file_name = f"{company}_history.pkl"
    df = pd.read_pickle(os.path.abspath("portfolio/pickles/{}".format(file_name)))
    df = df['Open'].values
    df = df.reshape(-1,1)

    dataset_train = np.array(df[:int(df.shape[0]*0.8)])
    dataset_test = np.array(df[int(df.shape[0]*0.8)-50:])

    scaler = MinMaxScaler(feature_range=(0,1))
    dataset_train = scaler.fit_transform(dataset_train)
    dataset_test = scaler.transform(dataset_test)

    def create_my_dataset (df):
        x = []
        y = []
        for i in range (50, df.shape[0]):
            x.append(df[i-50:i,0])
            y.append(df[i,0])
        x = np.array(x)
        y = np.array(y)
        return x,y

    x_train, y_train, = create_my_dataset(dataset_train)
    x_test, y_test, = create_my_dataset(dataset_test)

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=96, return_sequences=True, input_shape = (x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    if (not os.path.exists('stock_prediction.h5')):
        model.fit(x_train, y_train, epochs=5, batch_size=32)
        model.save('stock_prediction.h5')

    model = load_model('stock_prediction.h5')

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # fig, ax = plt.subplots(figsize=(16,9))
    # plt.plot(df, color = 'red', label = 'Original Stock Price')
    # ax.plot(range(len(y_train) + 50, len(y_train) + 50 + len(predictions)), predictions, color = 'blue', label = 'Predicted')
    # plt.legend()
    # plt.show()
    # print (predictions)
    
    
    # NOTE: Real
    y_test_scaled = scaler.inverse_transform(y_test.reshape(-1,1))
    # print(y_test_scaled)
    # fig, ax = plt.subplots(figsize=(16,9))
    # ax.plot(y_test_scaled, color = 'red', label = 'True Price')
    # plt.plot(predictions, color = 'blue', label = 'Predicted')
    # plt.legend()
    # plt.savefig('result.png')
    # plt.show()
    return predictions, y_test_scaled
