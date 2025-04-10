import streamlit as st
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class ACN:

    def __str__(self):
        return "ACN-Data dataset"

    @staticmethod
    def page():
        #st.set_option('deprecation.showPyplotGlobalUse', False)
        st.write("You have selected the ACN-Data dataset")
        link = "https://ev.caltech.edu/dataset"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

        site = st.selectbox("Select Site", ("caltech", "jpl", "office1"))

        with st.spinner('Loading...'):
            with open("./Data/ACN-Data/" + site + ".json") as f:
                data = json.load(f)

        # Convert dataset to a DataFrame
        df = pd.DataFrame(data['_items'])

        # Preprocess the data
        df['connectionTime'] = pd.to_datetime(df['connectionTime'])
        df['disconnectTime'] = pd.to_datetime(df['disconnectTime'])
        df['arrival_time'] = df['connectionTime'].dt.hour * 60 + df['connectionTime'].dt.minute
        df['departure_time'] = df['disconnectTime'].dt.hour * 60 + df['disconnectTime'].dt.minute
        df['charging_duration'] = (df['disconnectTime'] - df['connectionTime']).dt.total_seconds() / 3600
        df['weekday'] = df['connectionTime'].dt.dayofweek

        # Set the style
        sns.set(style="whitegrid")

        # Plot 1: Charging hours histogram
        st.title('Electric Vehicle Charging Data Visualization')
        st.subheader('1. Charging Hours Histogram')

        bin_edges = np.arange(0, df['charging_duration'].max() + 0.25, 0.25)
        fig, ax = plt.subplots()
        sns.histplot(data=df, x='charging_duration', bins=bin_edges, kde=False, ax=ax)

        ax.set_xlabel('Charging Time (hours)')
        ax.set_ylabel('Number of Sessions')
        plt.tight_layout()
        st.pyplot(fig)

        # Plot 2: Charging hours histogram for weekdays and weekends
        st.subheader('2. Charging Hours Histogram for Weekdays and Weekends')

        g = sns.FacetGrid(df, col='weekday', hue='weekday', sharex=False, sharey=False)
        g.map(sns.histplot, 'charging_duration', bins=bin_edges, kde=False)
        g.set_axis_labels('Charging Time (hours)', 'Number of Sessions')
        plt.tight_layout()
        st.pyplot(g.fig)

        # Plot 3: Arrival and departure times line graph
        st.subheader('3. Charging start and end times')

        bin_edges_arr_dep = np.arange(0, 24 * 60 + 15, 15)
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

        # Plot 4: Charging time vs energy charged
        st.subheader('4. Charging Time vs Energy Charged')

        bin_edges_charging = np.arange(0, df['charging_duration'].max() + 0.25, 0.25)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='charging_duration', y='kWhDelivered', ax=ax)

        ax.set_xlabel('Charging Time (hours)')
        ax.set_ylabel('Energy Charged (kWh)')
        plt.tight_layout()
        st.pyplot(fig)

        # Calculate mean connect not charging time
        df['doneChargingTime'] = pd.to_datetime(df['doneChargingTime'])
        connect_not_charging_duration = (df['disconnectTime'] - df['doneChargingTime']).dropna().dt.total_seconds() / 3600
        mean_connect_not_charging_duration = connect_not_charging_duration.mean()
        st.caption(f'Mean connect not charging time: {mean_connect_not_charging_duration:.2f} hours')

        # Plot 5: Energy charged vs number of sessions
        st.subheader('5. Energy Charged vs Number of Sessions')

        fig, ax = plt.subplots()
        sns.histplot(data=df, x='kWhDelivered', kde=False, ax=ax)

        ax.set_xlabel('Energy Charged (kWh)')
        ax.set_ylabel('Number of Sessions')
        plt.tight_layout()
        st.pyplot(fig)



