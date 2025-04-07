import streamlit as st
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class DOE:
    @staticmethod
    def page():
        st.write("You have selected the DOE dataset")
        st.write("This dataset contains information from 3,395 high resolution electric vehicle charging sessions. The workplace locations include: research and innovation centers, manufacturing, testing facilities and office headquarters.")
        link = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NFPQLW"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

        with st.spinner('Loading...'):
            data = pd.read_csv("./Data/DOE-Dataset/station_data_dataverse.csv", delimiter=",")

        data['created'] = pd.to_datetime(data['created'].apply(lambda t: t.split(' ')[1]))
        data['ended'] = pd.to_datetime(data['ended'].apply(lambda t: t.split(' ')[1]))

        data['arrival_time'] = data['created'].dt.hour * 60 + data['created'].dt.minute
        data['departure_time'] = data['ended'].dt.hour * 60 + data['ended'].dt.minute
        #################################################################
        st.subheader("1. Charging Hours Histogram")


        bin_edges = np.arange(0, data['chargeTimeHrs'].max() + 0.25, 0.25)
        fig, ax = plt.subplots()
        sns.histplot(data=data, x=data["chargeTimeHrs"],bins=bin_edges, kde=False, ax=ax)
        ax.set_xlabel("Charging Time (hours)")
        ax.set_ylabel("Number of Sessions")
        plt.tight_layout()
        st.pyplot(fig)
        #################################################################
        st.subheader("2. Charging start and end times")

        bin_edges_arr_dep = np.arange(0, 24 * 60 + 15, 15)
        arrival_counts, _ = np.histogram(data['arrival_time'], bins=bin_edges_arr_dep)
        departure_counts, _ = np.histogram(data['departure_time'], bins=bin_edges_arr_dep)
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

        #################################################################
        st.subheader("3. Charging Time vs Energy Charged")
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=data['chargeTimeHrs'], y='kwhTotal', ax=ax)

        ax.set_xlabel("Charging Time (hours)")
        ax.set_xlim(0, 15)

        ax.set_ylabel("Energy Charged (kWh)")
        #ax.set_ylim(0, 120)

        plt.tight_layout()
        st.pyplot(fig)

        #################################################################
        st.subheader("4. Energy Supplied Histogram")
        fig, ax = plt.subplots()

        sns.histplot(data=data, x='kwhTotal', kde=False, ax=ax)
        ax.set_xlabel("Energy Supplied (kWh)")
        ax.set_ylabel("Number of Events")
        plt.tight_layout()
        st.pyplot(fig)

