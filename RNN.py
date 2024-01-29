import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from math import sqrt
import holidays

# Load and preprocess data
df = pd.read_csv('your_dataset.csv')
df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)

# Add binary columns for holidays and weekends
# Add a binary column for weekends (1 for weekends, 0 for weekdays)
df['Weekend'] = df.index.weekday.isin([5, 6]).astype(int)

# Add a binary column for US holidays (you can change the country as needed)
us_holidays = holidays.UnitedStates()
df['Holiday'] = df.index.isin([date for date in us_holidays]).astype(int)

# Normalize the features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df.values)

# Function to create sequences for LSTM
def create_sequences(data, sequence_length):
    xs = []
    ys = []
    for i in range(len(data)-sequence_length):
        x = data[i:(i+sequence_length), :-1]
        y = data[i+sequence_length, -1]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

sequence_length = 144  # Adjust based on your sequence length
X, y = create_sequences(scaled_data, sequence_length)

# Split into train and test sets
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Build LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(LSTM(50))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Predictions
predicted = model.predict(X_test)
predicted = scaler.inverse_transform(np.concatenate((X_test[:, :, :-1], predicted), axis=2))[:, -1]

# Calculate performance metrics
actual = scaler.inverse_transform(scaled_data[train_size+sequence_length:])[:, -1]
mae = mean_absolute_error(actual, predicted)
rmse = sqrt(mean_squared_error(actual, predicted))

print(f'Mean Absolute Error (MAE): {mae}')
print(f'Root Mean Squared Error (RMSE): {rmse}')

# Plot training loss and validation loss
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()
