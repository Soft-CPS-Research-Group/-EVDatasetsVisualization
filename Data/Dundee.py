import pandas as pd
import streamlit as st
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

class Dundee:

    def __str__(self):
        return "Electric Vehicle Charging Sessions Dundee"

    @staticmethod
    def page():
        st.write("You have selected the Electric Vehicle Charging Sessions Dundee dataset")
        link = "https://data.dundeecity.gov.uk/dataset/ev-charging-data"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

        # Load dataset
        with st.spinner('Loading...'):
            data = pd.read_csv("./Data/Electric Vehicle Charging Sessions Dundee/cp-locations.csv")

        # Keep only the relevant columns (latitude and longitude)
        df = data[['Latitude', 'Longitude']]

        # Rename the columns to 'lat' and 'lon'
        df.columns = ['lat', 'lon']

        # Display the data on a map
        st.title("Chargers Location")
        st.map(df)

        file = st.selectbox("Select File", ("cp-data-jan-dec-2017", "cp-data-dec-mar-2018", "cp-data-mar-may-2018", "cp-data-jun-sep-2018" ))

        # Read the dataset into a DataFrame
        with st.spinner('Loading...'):
            df = pd.read_csv("./Data/Electric Vehicle Charging Sessions Dundee/"+file+".csv")

        df = df.dropna(subset=['Start Date', 'Start Time', 'End Date', 'End Time'])

        # Preprocessing and calculating relevant columns
        # Convert the date and time columns to datetime objects
        df['StartDatetime'] = pd.to_datetime(df['Start Date'] + ' ' + df['Start Time'],
                                                    format='%d/%m/%Y %H:%M')
        df['EndDatetime'] = pd.to_datetime(df['End Date'] + ' ' + df['End Time'],
                                                format='%d/%m/%Y %H:%M')

        # Calculate the charging duration in hours
        df['charging_duration'] = (df['EndDatetime'] - df['StartDatetime']).dt.seconds / 3600

        df['weekday'] = df['StartDatetime'].dt.dayofweek

        df['arrival_time'] = df['StartDatetime'].apply(lambda x: x.hour * 60 + x.minute)
        df['departure_time'] = df['EndDatetime'].apply(lambda x: x.hour * 60 + x.minute)

        # Plot 1: Charging hours histogram
        st.title('Electric Vehicle Charging Data Visualization')
        st.subheader('1. Charging Hours Histogram')

        charging_duration_median = df['charging_duration'].median()
        filtered_df = df[df['charging_duration'] <= charging_duration_median + 1000 / 60]  # Convert 1000 minutes to hours

        bin_edges = np.arange(0, filtered_df['charging_duration'].max() + 0.25, 0.25)
        fig, ax = plt.subplots()
        sns.histplot(data=filtered_df, x='charging_duration', bins=bin_edges, kde=False, ax=ax)

        ax.set_xlabel('Charging Time (hours)')
        ax.set_ylabel('Number of Sessions')
        plt.tight_layout()
        st.pyplot(fig)

        # Plot 2: Charging hours histogram for weekdays and weekends
        st.subheader('2. Charging Hours Histogram for Weekdays and Weekends')

        g = sns.FacetGrid(filtered_df, col='weekday', hue='weekday', sharex=False, sharey=False)
        g.map(sns.histplot, 'charging_duration', bins=bin_edges, kde=False)
        g.set_axis_labels('Charging Time (hours)', 'Number of Sessions')
        plt.tight_layout()
        st.pyplot(g.fig)

        # Plot 3: Arrival and departure times line graph
        st.subheader('3. Charging start and end times')

        bin_edges_arr_dep = np.arange(0, 24 * 60 + 60, 60)
        arrival_counts, _ = np.histogram(df['arrival_time'], bins=bin_edges_arr_dep)
        departure_counts, _ = np.histogram(df['departure_time'], bins=bin_edges_arr_dep)
        bin_centers = (bin_edges_arr_dep[:-1] + bin_edges_arr_dep[1:]) / 2

        fig, ax = plt.subplots()
        ax.plot(bin_centers, arrival_counts, label='Charging Start', color='blue')
        ax.plot(bin_centers, departure_counts, label='Charging End', color='red')

        ax.set_xlabel('Time (hours)')
        ax.set_xticks(np.arange(0, 24 * 60 + 60, 60))
        ax.set_xticklabels(np.arange(0, 25))
        ax.set_ylabel('Number of Sessions')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

        # Filter out outliers or incorrect data points
        filtered_df = df[(df['charging_duration'] >= 0) & (df['Total kWh'] >= 0) & (df['charging_duration'] < 1000)]

        # Plot 4: Charging Time vs Energy Charged with filtered data
        st.subheader('4. Charging Time (X) vs Energy Charged (Y)')

        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x='charging_duration', y='Total kWh', ax=ax)

        ax.set_xlabel('Charging Time (hours)')
        ax.set_ylabel('Energy Charged (kWh)')
        plt.tight_layout()
        st.pyplot(fig)

        # Plot 5: Energy Charged vs Number of Sessions
        st.subheader('5. Energy Charged (X) vs Number of Sessions (Y)')

        energy_bin_edges = np.arange(0, df['Total kWh'].max() + 1, 1)
        fig, ax = plt.subplots()
        sns.histplot(data=df, x='Total kWh', bins=energy_bin_edges, kde=False, ax=ax)

        ax.set_xlabel('Energy Charged (kWh)')
        ax.set_ylabel('Number of Sessions')
        plt.tight_layout()
        st.pyplot(fig)

