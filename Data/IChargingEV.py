import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class ICEV:
    def __str__(self):
        return "I-Charging"
    
    @staticmethod
    def page():
        st.write("You have selected the I-Charging EV dataset")

        with st.spinner('Loading...'):
            data = pd.read_csv("./Data/ICharging/icharging-treated-data.csv", delimiter=";")
        data['start.time'] = pd.to_datetime(data['start.time'], format="%d/%m/%Y %H:%M")
        data['end.time'] = pd.to_datetime(data['end.time'], format="%d/%m/%Y %H:%M")
        #################################################################
        st.subheader("1. Charging Hours Histogram")


        bin_edges = np.arange(0, 100 + .25, .25)
        fig, ax = plt.subplots()
        sns.histplot(data=data, x=data["duration"],bins=bin_edges, kde=False, ax=ax)
        ax.set_xlabel("Charging Time (hours)")
        ax.set_ylabel("Number of Sessions")
        plt.tight_layout()
        st.pyplot(fig)
        #################################################################
        st.subheader("2. Arriving and Departing Times")

        bin_edges_arr_dep = np.arange(0, 24 * 60 + 15, 15)
        arrival_counts, _ = np.histogram(data['start.time'].dt.time.apply(lambda t: t.hour * 60 + t.minute),
                                        bins=bin_edges_arr_dep)
        
        departure_counts, _ = np.histogram(data['end.time'].dt.time.apply(lambda t: t.hour * 60 + t.minute),
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

        #################################################################
        st.subheader("3. Charging Time vs Energy Charged")
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=data['duration'], y='energy', ax=ax)

        ax.set_xlabel("Charging Time (hours)")
        ax.set_xlim(0, 40)

        ax.set_ylabel("Energy Charged (kWh)")
        ax.set_ylim(0, 120)

        plt.tight_layout()
        st.pyplot(fig)

        #################################################################
        st.subheader("4. Energy Supplied Histogram")
        bin_edges_energy = np.arange(0, 150 + 1, 1)
        fig, ax = plt.subplots()
        sns.histplot(data=data, x='energy', bins=bin_edges_energy, kde=False, ax=ax)
        ax.set_xlabel("Energy Supplied (kWh)")
        ax.set_ylabel("Number of Events")
        plt.tight_layout()
        st.pyplot(fig)
