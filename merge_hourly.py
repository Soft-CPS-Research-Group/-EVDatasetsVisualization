import pandas as pd

# Load your dataset
# Assuming your dataset is in a CSV file named 'data.csv'
data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset.csv')

# Convert the 'Time' column to datetime
data['Time'] = pd.to_datetime(data['Time'])

# Set the 'Time' column as the index
data.set_index('Time', inplace=True)

# Group by hour and aggregate
hourly_data = data.resample('H').agg({
    'Total Occupied': 'max',
    'tempmax': 'mean',  # Modify aggregation as needed
    'tempmin': 'mean',  # Modify aggregation as needed
    'temp': 'mean',     # Modify aggregation as needed
    'precip': 'mean',   # Example for sum
    'precipprob': 'mean', # Example for mean
    "snow": "mean",
    "snowdepth": "mean"
})

print(hourly_data)

hourly_data.to_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset_hourly.csv', index=True)
