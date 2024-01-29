import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import holidays
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Load data
print("Loading data...")
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
data['Time'] = pd.to_datetime(data['Time'])
data.set_index('Time', inplace=True)

# Selecting the 'Total Occupied' column
ts = data['Total Occupied']

# Create binary columns for holidays and weekends
us_holidays = holidays.UnitedStates()
data['Holiday'] = data.index.isin([h for h in us_holidays]).astype(int)
data['Weekend'] = (data.index.weekday >= 5).astype(int)

# Include weather features
weather_features = ['tempmax', 'tempmin', 'temp', 'precip', 'precipprob', 'snow', 'snowdepth']

# Define target and exogenous variables (including weather features)
target = data['Total Occupied']
exog = data[['Holiday', 'Weekend'] + weather_features]

# Splitting the data into train and test sets
split_point = int(len(ts) * 0.8)
train, test = ts[0:split_point], ts[split_point:]
train_exog, test_exog = data[['Holiday', 'Weekend']][0:split_point], data[['Holiday', 'Weekend']][split_point:]
print("Data split into training and testing sets.")

# Define SARIMAX model parameters
order = (1, 1, 1)
seasonal_order = (1, 1, 1, 24)

# Fit SARIMAX model on training data
print("Fitting SARIMAX model on training data...")
model = SARIMAX(train, exog=train_exog, order=order, seasonal_order=seasonal_order)
model_fit = model.fit()

# Predictions for the next 24 hours
next_24_hours_exog = test_exog.iloc[:24]
predictions = model_fit.forecast(steps=24, exog=next_24_hours_exog)
actual = test.iloc[:24]
next_24_hours_index = test.index[:24]

# Calculate performance metrics
mse = mean_squared_error(actual, predictions)
mae = mean_absolute_error(actual, predictions)
rmse = np.sqrt(mse)
smape_value = 100/len(actual) * np.sum(2 * np.abs(predictions - actual) / (np.abs(actual) + np.abs(predictions)))

print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'Root Mean Squared Error: {rmse}')
print(f'Symmetric Mean Absolute Percentage Error: {smape_value}%')

# Plotting the results for the last week and the next 24 hours
print("Plotting the results for the last week and the next 24 hours...")
plt.figure(figsize=(12,6))
last_week_train_index = train.index[-7*24:]  # last week of training data
last_week_train = train.iloc[-7*24:]
plt.plot(last_week_train_index, last_week_train, label='Train (Last Week)')
plt.plot(next_24_hours_index, actual, label='Test (Actual Next 24 Hours)')
plt.plot(next_24_hours_index, predictions, label='SARIMAX Predictions', color='red')
plt.title('SARIMAX Model Predictions for Next 24 Hours with Last Week Data')
plt.xlabel('Time')
plt.ylabel('Total Occupied')
plt.legend()
plt.show()








import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import itertools
import holidays

# Load data
print("Loading data...")
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
data['Time'] = pd.to_datetime(data['Time'])
data.set_index('Time', inplace=True)

# Selecting the 'Total Occupied' column
ts = data['Total Occupied']

# Create binary columns for holidays and weekends
us_holidays = holidays.UnitedStates()
data['Holiday'] = data.index.isin([h for h in us_holidays]).astype(int)
data['Weekend'] = (data.index.weekday >= 5).astype(int)

# Include weather features
weather_features = ['tempmax', 'tempmin', 'temp', 'precip', 'precipprob', 'snow', 'snowdepth']

# Define target and exogenous variables (including weather features)
target = data['Total Occupied']
exog = data[['Holiday', 'Weekend'] + weather_features]

# Split data into train and test sets
split_point = int(len(target) * 0.8)
train, test = target[0:split_point], target[split_point:]
train_exog, test_exog = exog[0:split_point], exog[split_point:]

print("Data split into training and testing sets.")

# Hyperparameter Optimization for SARIMAX (p, d, q, P, D, Q, s)
p = d = q = P = D = Q = range(0, 2)
s = 24  # Assuming daily seasonality from analysis
seasonal_pdq = [(x[0], x[1], x[2], s) for x in list(itertools.product(p, d, q))]
pdq = list(itertools.product(p, d, q, P, D, Q))

best_aic = np.inf
best_params = None
best_seasonal_params = None
best_model = None

print("Optimizing SARIMAX hyperparameters...")
for param in pdq:
    for seasonal_param in seasonal_pdq:
        try:
            model = SARIMAX(train, exog=train_exog, order=param, seasonal_order=seasonal_param)
            results = model.fit()
            if results.aic < best_aic:
                best_aic = results.aic
                best_params = param
                best_seasonal_params = seasonal_param
                best_model = results
        except:
            continue
print(f"Best SARIMAX{best_params}x{best_seasonal_params} model AIC: {best_aic}")

# Rolling Forecast
history = [x for x in train]
predictions = list()
test_index = test.index
print("Starting rolling forecast...")
for t in range(len(test)):
    model = SARIMAX(history, exog=train_exog, order=best_params, seasonal_order=best_seasonal_params)
    model_fit = model.fit()
    output = model_fit.forecast(exog=test_exog.iloc[t:t+1])  # Provide exogenous variables for forecasting
    yhat = output.values[0]
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
plt.plot(test_index, predictions, label='SARIMAX Predictions', color='red')
plt.title('SARIMAX Rolling Forecast')
plt.xlabel('Time')
plt.ylabel('Total Occupied')
plt.legend()
plt.show()
