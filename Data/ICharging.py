import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

# Function to create visualizations
def create_visualizations(data):
    # Filter the data for charging events
    charging_data = data[data['status'] == 10]

    # Plot energy vs time
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.scatter(charging_data['localtime (s)'], charging_data['energy (kWh)'])
    ax1.set_xlabel('Charging Time (s)')
    ax1.set_ylabel('Energy (kWh)')
    ax1.set_title('Energy vs Charging Time')
    ax1.grid(True)

    # Plot power vs time
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.scatter(charging_data['localtime (s)'], charging_data['power (kW)'])
    ax2.set_xlabel('Charging Time (s)')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Power vs Charging Time')
    ax2.grid(True)

    # Plot SOC vs time
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.scatter(charging_data['localtime (s)'], charging_data['soc (0-100%)'])
    ax3.set_xlabel('Charging Time (s)')
    ax3.set_ylabel('State of Charge (0-100%)')
    ax3.set_title('State of Charge vs Charging Time')
    ax3.grid(True)

    # Count charging events per connector type
    connector_counts = charging_data['type (CCS, CHAdeMO)'].value_counts()

    # Plot connector type distribution
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    connector_counts.plot(kind='bar', ax=ax4)
    ax4.set_xlabel('Connector Type')
    ax4.set_ylabel('Number of Charging Events')
    ax4.set_title('Connector Type Distribution')
    ax4.set_xticklabels(['CCS1', 'CCS2', 'CHAdeMO'])
    ax4.grid(axis='y')

    return fig1, fig2, fig3, fig4

def page():
    st.subheader("You have selected the I-Charging dataset")
    # Streamlit app
    st.title("EV Charging Data Visualization")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, sep=";", index_col=False)
        fig1, fig2, fig3, fig4 = create_visualizations(data)

        st.header("Energy vs Charging Time")
        st.pyplot(fig1)

        st.header("Power vs Charging Time")
        st.pyplot(fig2)

        st.header("State of Charge vs Charging Time")
        st.pyplot(fig3)

        st.header("Connector Type Distribution")
        st.pyplot(fig4)
    else:
        st.write("Please upload a CSV file to visualize the data.")
