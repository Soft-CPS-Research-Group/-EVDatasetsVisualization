import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class Boulder:

    def __str__(self):
        return "City of Boulder Electric Vehicle Charging Station Energy Consumption"
    
    @staticmethod
    def page():
        st.write("You have selected the City of Boulder Electric Vehicle Charging Station Energy Consumption dataset")
        link = "https://open-data.bouldercolorado.gov/datasets/39288b03f8d54b39848a2df9f1c5fca2_0/about"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

        # Load dataset
        with st.spinner('Loading...'):
            data = pd.read_csv("./Data/City of Boulder Electric Vehicle Charging Station Energy Consumption/Electric_Vehicle_Charging_Station_Energy_Consumption.csv")

        # Process data
        data['Start_Date___Time'] = pd.to_datetime(data['Start_Date___Time'])
        data['End_Date___Time'] = pd.to_datetime(data['End_Date___Time'])
        data['Charging_Time'] = pd.to_timedelta(data['Charging_Time__hh_mm_ss_'])
        data['weekday'] = data['Start_Date___Time'].dt.dayofweek

        # Create bins
        bins = pd.timedelta_range(start='0 minutes', end='24 hours', freq='15T')

        # Visualizations

        st.subheader("1. Charging Hours Histogram")
        bin_edges = np.arange(0, data['Charging_Time'].dt.total_seconds().max() / 3600 + 0.25, 0.25)
        fig, ax = plt.subplots()
        sns.histplot(data=data, x=data['Charging_Time'].dt.total_seconds() / 3600, bins=bin_edges, kde=False, ax=ax)
        ax.set_xlabel("Charging Time (hours)")
        ax.set_ylabel("Number of Sessions")
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("2. Charging Hours Histogram (Weekdays vs Weekends)")
        weekday_data = pd.cut(data[data['weekday'] < 5]['Charging_Time'].dt.total_seconds() / 3600,
                            bins=pd.interval_range(start=0, end=24, freq=0.25)).value_counts().sort_index()
        weekend_data = pd.cut(data[data['weekday'] >= 5]['Charging_Time'].dt.total_seconds() / 3600,
                            bins=pd.interval_range(start=0, end=24, freq=0.25)).value_counts().sort_index()
        fig, ax = plt.subplots()

        midpoints = [(interval.left + interval.right) / 2 for interval in weekday_data.index]
        plt.plot(midpoints, weekday_data.values, label='Weekdays')

        midpoints = [(interval.left + interval.right) / 2 for interval in weekend_data.index]
        plt.plot(midpoints, weekend_data.values, label='Weekends')

        ax.set_xlabel("Charging Time (hours)")
        ax.set_ylabel("Number of Charging Sessions")
        plt.legend()
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("3. Charging start and end times")

        bin_edges_arr_dep = np.arange(0, 24 * 60 + 15, 15)
        arrival_counts, _ = np.histogram(data['Start_Date___Time'].dt.time.apply(lambda t: t.hour * 60 + t.minute),
                                        bins=bin_edges_arr_dep)
        departure_counts, _ = np.histogram(data['End_Date___Time'].dt.time.apply(lambda t: t.hour * 60 + t.minute),
                                        bins=bin_edges_arr_dep)
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

        st.subheader("4. Charging Time vs Energy Charged")

        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=data['Charging_Time'].dt.total_seconds() / 3600, y='Energy__kWh_', ax=ax)

        ax.set_xlabel("Charging Time (hours)")
        ax.set_ylabel("Energy Charged (kWh)")
        plt.tight_layout()
        st.pyplot(fig)



        st.subheader("5. Energy Supplied Histogram")
        bin_edges_energy = np.arange(0, data['Energy__kWh_'].max() + 1, 1)
        fig, ax = plt.subplots()
        sns.histplot(data=data, x='Energy__kWh_', bins=bin_edges_energy, kde=False, ax=ax)
        ax.set_xlabel("Energy Supplied (kWh)")
        ax.set_ylabel("Number of Events")
        plt.tight_layout()
        st.pyplot(fig)


