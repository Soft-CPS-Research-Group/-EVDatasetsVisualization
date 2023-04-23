import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def page():
    st.write("You have selected the City of Palo Alto - Perth & Kinross Council's Electric Vehicle Charging Station Usage dataset")
    link = "https://data.cityofpaloalto.org/dataviews/257812/ELECT-VEHIC-CHARG-STATI-83602/"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

    # Load the data
    data = pd.read_csv("./Data/City of Palo Alto - Electric Vehicle Charging Station Usage/ChargePoint Data CY20Q4.csv")

    # Convert charging time to timedelta
    data['Charging_Time'] = pd.to_timedelta(data['Charging Time (hh:mm:ss)'])

    # Convert date columns to datetime objects
    data['Start_Date'] = pd.to_datetime(data['Start Date'])
    data['End_Date'] = pd.to_datetime(data['End Date'])

    # Graph 1: Charging Hours Histogram
    st.title('Electric Vehicle Charging Data Visualization')
    st.subheader('1. Charging Hours Histogram')

    bin_edges = np.arange(0, data['Charging_Time'].dt.total_seconds().max() / 3600 + 0.25, 0.25)
    fig, ax = plt.subplots()
    sns.histplot(data=data, x=data['Charging_Time'].dt.total_seconds() / 3600, bins=bin_edges, kde=False, ax=ax)

    ax.set_xlabel('Charging Time (hours)')
    ax.set_ylabel('Number of Sessions')
    plt.tight_layout()
    st.pyplot(fig)

    # Graph 2: Charging Sessions by Day of the Week
    st.subheader('2. Charging Sessions by Day of the Week')

    day_of_week = data['Start_Date'].dt.dayofweek
    day_counts = day_of_week.value_counts().sort_index()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig, ax = plt.subplots()
    sns.barplot(x=day_names, y=day_counts, ax=ax)

    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Number of Sessions')
    plt.tight_layout()
    st.pyplot(fig)

    # Graph 3: Arrival and Departure Times Line Graph
    st.subheader('3. Arrival and Departure Times Line Graph')

    bin_edges_arr_dep = np.arange(0, 24 * 60 + 15, 15)
    arrival_counts, _ = np.histogram(data['Start_Date'].dt.hour * 60 + data['Start_Date'].dt.minute,
                                     bins=bin_edges_arr_dep)
    departure_counts, _ = np.histogram(data['End_Date'].dt.hour * 60 + data['End_Date'].dt.minute,
                                       bins=bin_edges_arr_dep)
    bin_centers = (bin_edges_arr_dep[:-1] + bin_edges_arr_dep[1:]) / 2

    fig, ax = plt.subplots()
    ax.plot(bin_centers, arrival_counts, label='Arrival Time', color='blue')
    ax.plot(bin_centers, departure_counts, label='Departure Time', color='red')

    ax.set_xlabel('Time (hours)')
    ax.set_xticks(np.arange(0, 24 * 60 + 60, 60))
    ax.set_xticklabels(np.arange(0, 25))
    ax.set_ylabel('Number of Sessions')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

    # Graph 4: Charging Time vs Energy Charged
    st.subheader('4. Charging Time vs Energy Charged')

    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x=data['Charging_Time'].dt.total_seconds() / 3600, y='Energy (kWh)', ax=ax)

    ax.set_xlabel('Charging Time (hours)')
    ax.set_ylabel('Energy Charged (kWh)')
    plt.tight_layout()
    st.pyplot(fig)

    # Graph 5: Energy Charged vs GHG Savings
    st.subheader('5. Energy Charged vs GHG Savings')

    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='Energy (kWh)', y='GHG Savings (kg)', ax=ax)

    ax.set_xlabel('Energy Charged (kWh)')
    ax.set_ylabel('GHG Savings (kg)')
    plt.tight_layout()
    st.pyplot(fig)
