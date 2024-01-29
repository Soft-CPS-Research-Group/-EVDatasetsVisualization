import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import itertools
import warnings

# Load data
print("Loading data...")
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
data['Time'] = pd.to_datetime(data['Time'])
data.set_index('Time', inplace=True)

# Selecting the 'Total Occupied' column
ts = data['Total Occupied']

# Splitting the data into train and test sets
split_point = int(len(ts) * 0.8)
train, test = ts[0:split_point], ts[split_point:]
print("Data split into training and testing sets.")

# Hyperparameter Optimization for ARIMA (p, d, q)
p = [1, 2]
d = [1, 2]
q = [0, 1]
pdq = list(itertools.product(p, d, q))

best_aic = np.inf
best_pdq = None
best_model = None

warnings.filterwarnings("ignore")

print("Optimizing ARIMA hyperparameters...")
for param in pdq:
    try:
        model = ARIMA(train, order=param)
        results = model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_pdq = param
            best_model = results
    except:
        continue
print(f"Best ARIMA{best_pdq} model AIC: {best_aic}")

# Fit ARIMA model on training data
print("Fitting ARIMA model on training data...")
best_model = ARIMA(train, order=best_pdq).fit()

# Predictions
predictions = best_model.forecast(steps=len(test))
test_index = test.index

# Performance Metrics
print("Calculating performance metrics...")
mse = mean_squared_error(test, predictions)
mae = mean_absolute_error(test, predictions)
rmse = np.sqrt(mse)
smape_value = 100/len(test) * np.sum(2 * np.abs(predictions - test) / (np.abs(test) + np.abs(predictions)))

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Symmetric Mean Absolute Percentage Error: {smape_value}')

# Plotting the results
print("Plotting the results...")
plt.figure(figsize=(12,6))
plt.plot(train.index, train, label='Train')
plt.plot(test_index, test, label='Test')
plt.plot(test_index, predictions, label='ARIMA Predictions', color='red')
plt.title('ARIMA Model Predictions')
plt.xlabel('Time')
plt.ylabel('Total Occupied')
plt.legend()
plt.show()




print(f"Best ARIMA{best_pdq} model AIC: {best_aic}")
# Store the best model parameters
best_order = best_pdq

# Rolling Forecast
history = [x for x in train]
predictions = list()
test_index = test.index
print("Starting rolling forecast...")
for t in range(len(test)):
    model = ARIMA(history, order=best_order)
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    history.append(test[t])  # Add actual observation to history for the next loop
    print(f'Predicted={yhat}, Expected={test[t]}')

# Performance Metrics
print("Calculating performance metrics...")
mse = mean_squared_error(test, predictions)
mae = mean_absolute_error(test, predictions)
rmse = np.sqrt(mse)
smape_value = 100/len(test) * np.sum(2 * np.abs(predictions - test) / (np.abs(test) + np.abs(predictions)))

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Symmetric Mean Absolute Percentage Error: {smape_value}')

# Plotting the results
print("Plotting the results...")
plt.figure(figsize=(12,6))
plt.plot(train.index, train, label='Train')
plt.plot(test_index, test, label='Test')
plt.plot(test_index, predictions, label='ARIMA Predictions', color='red')
plt.title('ARIMA Rolling Forecast')
plt.xlabel('Time')
plt.ylabel('Total Occupied')
plt.legend()
plt.show()