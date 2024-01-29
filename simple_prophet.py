from prophet import Prophet
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

# Load the same dataset
print("Loading data...")
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
data['Time'] = pd.to_datetime(data['Time'])
data.set_index('Time', inplace=True)

# Preparing the dataset for Prophet
df = data.reset_index().rename(columns={'Time': 'ds', 'Total Occupied': 'y'})

# Split the data into train and test sets
split_point = int(len(df) * 0.8)
train_df = df[:split_point]
test_df = df[split_point:]

# Initialize and fit the Prophet model
model = Prophet()
model.fit(train_df)

# Create a future dataframe and predict
future = model.make_future_dataframe(periods=len(test_df), freq='H')
forecast = model.predict(future)

# Extract predicted and actual values
predicted = forecast['yhat'][split_point:]
actual = test_df['y']

# Calculate performance metrics
mae = mean_absolute_error(actual, predicted)
rmse = sqrt(mean_squared_error(actual, predicted))
smape_value = 100/len(actual) * np.sum(2 * np.abs(predicted - actual) / (np.abs(actual) + np.abs(predicted)))

print(f'Mean Absolute Error (MAE): {mae}')
print(f'Root Mean Squared Error (RMSE): {rmse}')
print(f'Symmetric Mean Absolute Percentage Error (SMAPE): {smape_value}')

# Plot the forecast
fig1 = model.plot(forecast)
plt.title('Prophet Forecast with Train/Test Split')
plt.show()

# Plot components
fig2 = model.plot_components(forecast)
