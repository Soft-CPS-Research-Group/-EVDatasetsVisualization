from prophet import Prophet
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from math import sqrt
import holidays
import numpy as np

# Load and prepare the dataset
df = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
df['Time'] = pd.to_datetime(df['Time'])
df = df.rename(columns={'Time': 'ds', 'Total Occupied': 'y'})

# Add a binary indicator for weekends
df['is_weekend'] = df['ds'].dt.weekday.isin([5, 6]).astype(int)

# Include weather variables and the weekend indicator as additional regressors
weather_features = ['tempmax', 'tempmin', 'temp', 'precip', 'precipprob', 'snow', 'snowdepth'] + ['is_weekend']

# Initialize the Prophet model and add features as regressors
model = Prophet()
for feature in weather_features:
    model.add_regressor(feature)

# Add holidays
us_holidays = holidays.UnitedStates()
df['holiday'] = df['ds'].apply(lambda x: us_holidays.get(x, default='None'))
model.add_country_holidays(country_name='US')

# Split the data into train and test sets
test_size = 144  # The number of periods to predict
train_df = df[:-test_size]
test_df = df[-test_size:]

# Fit the model
model.fit(train_df)

# Create a future dataframe for predictions
future = model.make_future_dataframe(periods=test_size, freq='10min')

# Include weather variables and weekend indicator in the future dataframe
for feature in weather_features:
    future[feature] = df[feature]

# Predict
forecast = model.predict(future)

# Evaluate the model
predicted = forecast['yhat'][-test_size:]
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
plt.title('Prophet Forecast with Weather Variables, Holidays, and Weekends')
plt.show()

# Plot components
fig2 = model.plot_components(forecast)



