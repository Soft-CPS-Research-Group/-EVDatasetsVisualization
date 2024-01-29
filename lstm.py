import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import holidays

# Load and preprocess data
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
data['Time'] = pd.to_datetime(data['Time'])
data.set_index('Time', inplace=True)
ts = data['Total Occupied'].values
ts = ts.reshape(-1, 1)

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
ts_scaled = scaler.fit_transform(ts)

# Function to create a dataset for LSTM
def create_dataset(data, look_back=1):
    X, Y = [], []
    for i in range(len(data) - look_back):
        a = data[i:(i + look_back), 0]
        X.append(a)
        Y.append(data[i + look_back, 0])
    return np.array(X), np.array(Y)

# Split into train and test sets
look_back = 24
train_size = int(len(ts_scaled) * 0.8)
test_size = len(ts_scaled) - train_size
train, test = ts_scaled[0:train_size,:], ts_scaled[train_size - look_back:len(ts_scaled),:]
X_train, Y_train = create_dataset(train, look_back)
X_test, Y_test = create_dataset(test, look_back)

# Reshape input to be [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Create and fit the LSTM network
model = Sequential()
model.add(LSTM(50, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, Y_train, epochs=5, batch_size=1, verbose=2)

# Make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Invert predictions
train_predict = scaler.inverse_transform(train_predict)
Y_train = scaler.inverse_transform([Y_train])
test_predict = scaler.inverse_transform(test_predict)
Y_test = scaler.inverse_transform([Y_test])

# Calculate performance metrics
train_score_rmse = np.sqrt(mean_squared_error(Y_train[0], train_predict[:,0]))
print(f'Train Score: {train_score_rmse:.2f} RMSE')
test_score_rmse = np.sqrt(mean_squared_error(Y_test[0], test_predict[:,0]))
print(f'Test Score: {test_score_rmse:.2f} RMSE')

# Plot training data and predictions
plt.figure(figsize=(12,6))
plt.plot(data.index[:len(train_predict)], train_predict.flatten(), label='Train Predictions')
plt.plot(data.index[len(train_predict):(len(train_predict) + len(test_predict))], test_predict.flatten(), label='Test Predictions')
plt.plot(data.index, ts, label='Actual Data', alpha=0.3)
plt.title('LSTM Predictions vs Actual Data')
plt.xlabel('Time')
plt.ylabel('Total Occupied')
plt.legend()
plt.show()
