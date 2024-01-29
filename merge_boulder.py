import pandas as pd

# Load the datasets
weather_df = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/boulder_weather.csv')
occupancy_df = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/Total_Occupancy_Summary.csv')

# Convert the datetime columns to pandas datetime format and create a new 'Date' column for merging
weather_df['datetime'] = pd.to_datetime(weather_df['datetime']).dt.date
occupancy_df['Time'] = pd.to_datetime(occupancy_df['Time']).dt.tz_localize(None)
occupancy_df['Date'] = occupancy_df['Time'].dt.date

# Merge the datasets using the 'Date' column for alignment
merged_df = pd.merge(occupancy_df, weather_df, left_on='Date', right_on='datetime', how='left')

# Select relevant columns and include the original 'Time' column
final_df = merged_df[['Time', 'Total Occupied', 'tempmax', 'tempmin', 'temp', 'precip', 'precipprob', 'snow', 'snowdepth']]

# Save the new dataset to a CSV file
final_df.to_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/merged_dataset.csv', index=False)



