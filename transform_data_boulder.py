import pandas as pd


#CITY OF BOULDER
# Load the dataset
ev_charging_data = pd.read_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/Electric_Vehicle_Charging_Station_Energy_Consumption.csv')

# Convert the Start and End times to datetime
ev_charging_data['Start_Date___Time'] = pd.to_datetime(ev_charging_data['Start_Date___Time'])
ev_charging_data['End_Date___Time'] = pd.to_datetime(ev_charging_data['End_Date___Time'])

# Get unique station names
station_names = ev_charging_data['Station_Name'].unique()

# Initialize a dictionary to hold a DataFrame for each station
station_time_series = {}
start_date = ev_charging_data['Start_Date___Time'].min().floor('10T')
end_date = ev_charging_data['End_Date___Time'].max().ceil('10T')
# Create a time series DataFrame for each station
for station in station_names:
    # Filter data for the current station
    station_data = ev_charging_data[ev_charging_data['Station_Name'] == station]

    # Create a new DataFrame for the 15-minute time slots
    time_slots = pd.date_range(start=start_date, end=end_date, freq='10T')

    # Initialize a DataFrame with time slots and a column for occupancy
    time_series = pd.DataFrame(time_slots, columns=['Time'])
    time_series['Occupied'] = 0

    # Count the number of occupied slots for each time interval
    for _, row in station_data.iterrows():
        # Find the time slots that overlap with the charging session
        mask = (time_series['Time'] >= row['Start_Date___Time']) & (time_series['Time'] < row['End_Date___Time'])
        time_series.loc[mask, 'Occupied'] += 1

    # Add the DataFrame to the dictionary
    station_time_series[station] = time_series

# Example: Display the first few rows of the time series for the first station
print(station_time_series[station_names[0]].head())
print(station_time_series)

# Iterate through the station_time_series dictionary
for station, df in station_time_series.items():
    # Format the station name to be used in the file name (replace spaces and slashes)
    formatted_station_name = station.replace(" / ", "_").replace(" ", "_")

    # Define the file path for the CSV
    file_path = f'./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/{formatted_station_name}_time_series.csv'

    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

print("All DataFrames have been saved as CSV files.")


import matplotlib.pyplot as plt

# Example: Plot a line graph for the first station
station = station_names[0]
df = station_time_series[station]

plt.figure(figsize=(12, 6))
plt.plot(df['Time'], df['Occupied'])
plt.title(f"Occupancy Over Time for {station}")
plt.xlabel('Time')
plt.ylabel('Number of Occupied Slots')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Initialize a DataFrame for the summary
summarized_occupancy = pd.DataFrame(time_slots, columns=['Time'])
summarized_occupancy['Total Occupied'] = 0

# Sum the occurrences across all stations
for df in station_time_series.values():
    summarized_occupancy['Total Occupied'] += df['Occupied']

# Save the summarized DataFrame to CSV
summarized_occupancy.to_csv('./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/Total_Occupancy_Summary.csv', index=False)

# Example: Plot a line graph for the summarized data
plt.figure(figsize=(12, 6))
plt.plot(summarized_occupancy['Time'], summarized_occupancy['Total Occupied'])
plt.title("Total Occupancy Over Time Across All Stations")
plt.xlabel('Time')
plt.ylabel('Total Number of Occupied Slots')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
