import streamlit as st
import pandas as pd
import plotly.express as px  # Import Plotly Express
from datetime import datetime, date, timedelta


class ICharging:

    def __str__(self):
        return "I-Charging"
    
    @staticmethod
    def page():
        st.subheader("You have selected the I-Charging dataset")
        # Streamlit app
        st.title("EV Charging Data Visualization")

        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file, sep=";")

            # Add a Streamlit widget to let users choose the serial number
            serial_numbers = data['serialnumber'].unique()
            selected_serial_number = st.selectbox('Select a serial number:', sorted(serial_numbers))

            # Pass the selected serial number to the function
            fig1, fig2, fig3 = create_visualizations(data, selected_serial_number)

            st.header("Energy vs Charging Time")
            st.plotly_chart(fig1)

            st.header("Power vs Charging Time")
            st.plotly_chart(fig2)

            st.header("State of Charge vs Charging Time")
            st.plotly_chart(fig3)

        else:
            st.write("Please upload a CSV file to visualize the data.")


# Update the function to accept the selected serial number
def create_visualizations(data, selected_serial_number):
    # Filter the data for charging events
    charging_data = data[data['status'] == 10]

    # Filter the data by the selected serial number
    charging_data = charging_data[charging_data['serialnumber'] == selected_serial_number]

    # Find the rows where the value of 'soc' decreases
    mask = charging_data['soc (0-100%)'].diff() < 0

    # Create a new column 'event_id' and increment the ID each time there's a decrease in 'soc'
    charging_data['event_id'] = mask.cumsum()

    # Label the events with a unique ID
    charging_data['event_id'] = 'event_' + charging_data['event_id'].astype(str)

    serial_numbers = charging_data['event_id'].unique()
    selected_event_id = st.selectbox('Select a charging event:', sorted(serial_numbers))

    filtered_charging_data = charging_data[charging_data['event_id'] == selected_event_id]

    # Create Plotly Express visualizations
    fig1 = px.scatter(filtered_charging_data, x='localtime (s)', y='energy (kWh)', title='Energy vs Charging Time')
    fig2 = px.scatter(filtered_charging_data, x='localtime (s)', y='power (kW)', title='Power vs Charging Time')
    fig3 = px.scatter(filtered_charging_data, x='soc (0-100%)', y='power (kW)', title='State of Charge vs Power')

    return fig1, fig2, fig3