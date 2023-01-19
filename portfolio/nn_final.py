import os
import time
import warnings
import matplotlib.pyplot as plt
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.layers import Dense
from keras.models import Sequential
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error  # added builtin function to test the models
from sklearn.preprocessing import MinMaxScaler  # scaling the feature is THE MOST IMPORTANT task
from tensorflow import keras # Import

warnings.filterwarnings("ignore")
def run_neural(csv_file):
      # read the pickle file and filled missing values
      features = pd.read_pickle(os.getcwd() + "/portfolio/rf_pickles/final_df.pkl")
      features.fillna(0, inplace=True)
      labels = np.array(features.iloc[:, 22])
      features = features.drop(features.columns[22], axis=1)
      feature_list = list(features.columns)
      features = np.array(features)

      # Split the data into training and testing sets
      train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25,
                                                                              random_state=42)

      # scaling the data
      scaler = MinMaxScaler()
      scaler.fit(train_features)
      train_features = scaler.transform(train_features)
      test_features = scaler.transform(test_features)

      # time-track
      start_time = time.time()

      # created ML model
      rf = RandomForestRegressor(n_estimators=2000, random_state=42)

      # fit the model
      rf.fit(train_features, train_labels)
      # Use the forest's predict method on the test data
      predictions = rf.predict(test_features)

      print('Mean Absolute Error:',
            mean_absolute_error(test_labels, predictions))  # its recommended to use built in function for efficiency

      # time requied to train the model
      print("Time required {}".format(time.time() - start_time))

      # save model
      joblib.dump(rf, os.getcwd() + "/portfolio/saved_models/random_forest.joblib")

      # load model and predict its output
      model = joblib.load(os.getcwd() + "/portfolio/saved_models/random_forest.joblib")

      # read test csv file
      test = pd.read_csv(os.getcwd() + '/portfolio/test_csv_nn/{}'.format(csv_file))
      test = scaler.transform(test)  # scaling the test data
      y_pred = model.predict(test)
      print("Prediction Of loaded model ", y_pred)
      print("\n\n\n\n\n")

      X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.1)

      scaler = MinMaxScaler()
      scaler.fit(X_train)
      X_train = scaler.transform(X_train)
      X_test = scaler.transform(X_test)

      # define Neural network architecture
      model = Sequential()
      model.add(Dense(10, activation='relu'))
      model.add(Dense(1, activation='linear'))
      adam = tf.keras.optimizers.Adam(lr=0.001)

      # compile the model
      model.compile(loss='mae', metrics=['mae'], optimizer=adam)

      # time track
      start_time = time.time()

      # fit the model
      history = model.fit(X_train, y_train, epochs=100)
      print("Time required {}".format(time.time() - start_time))
      # print(history)
      # print(history.history)
      # pd.DataFrame(history.history).plot(figsize = (8,5))
      # plt.grid(True)
      # plt.show()

      # save model
      model.save(os.getcwd() + "/portfolio/saved_models/Neural_Network")

      model.summary()
      observed = model.predict(X_test)
      ### Predict
      model = keras.models.load_model(os.getcwd() + "/portfolio/saved_models/Neural_Network")
      # read test csv file
      test = pd.read_csv(os.getcwd() + '/portfolio/test_csv_nn/{}'.format(csv_file))

      y_pred = model.predict(scaler.transform(test))

      print("Prediction Of loaded model ", y_pred)
      #LSTM 
      #61.97
      return y_pred, history.history