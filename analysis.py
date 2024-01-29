import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose

# Load data
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv')
data['Time'] = pd.to_datetime(data['Time'])
data.set_index('Time', inplace=True)

# Selecting the 'Total Occupied' column
ts = data['Total Occupied']

# ACF and PACF plots
plt.figure(figsize=(12, 5))
plt.subplot(121)
plot_acf(ts, ax=plt.gca(), lags=100)
plt.subplot(122)
plot_pacf(ts, ax=plt.gca(), lags=100)
plt.show()

# Seasonal Decomposition
# Assuming hourly data, you might want to change the 'period' parameter
# based on the seasonality you expect in your data.
result = seasonal_decompose(ts, model='additive', period=24)  # Change '24' if a different seasonality is expected
result.plot()
plt.show()