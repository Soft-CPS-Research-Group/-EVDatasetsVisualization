import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, date, timedelta

class Pecan:

    def __str__(self):
        return "Pecan Street"


    @staticmethod
    def page():
        st.subheader("You have selected the Pecan Street dataset")
        link = "https://www.pecanstreet.org/"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

        st.write("Due to the size of the files this vizualization might not work. Please go to the official dataset website and download the files corresponding to the data you want to vizualize in 15 and 1 minute granularity. Then download this code from its official repo and use the files")

        location = st.selectbox("Select Granularity", ("newyork", "california", "austin"))

        if location == "california":
            st.error("California data does not include EVs")
        else:
            gran = st.selectbox("Select Granularity", ("15min", "1min"))

            try:
                if gran == "15min":
                    # Read the data from a CSV file
                    df = pd.read_csv('./Data/PecanStreet/' + location + '/15minute_data_' + location + '/15minute_data.csv')
                    var = 'local_15min'
                elif gran == "1min":
                    # Read the data from a CSV file
                    with st.spinner('Loading...'):
                        df = pd.read_csv('./Data/PecanStreet/' + location + '/1minute_data_' + location + '/1minute_data.csv')
                    var = 'localminute'
            except:
                st.error("Pecan street data is currently unavailable 🫤")
                return

            # dropping rows for column a and b
            df = df.dropna(subset=['car1', 'car2'], how='all')

            # Get a list of available buildings (dataid)
            buildings = df['dataid'].unique()

            # Create a Streamlit selectbox for choosing a building
            selected_building = st.selectbox('Select a building', buildings)

            # Filter the data by the selected building and car1/car2 columns
            cars = df.loc[df['dataid'] == selected_building, [var, 'car1', 'car2']].dropna(how="all")

            # Sort the data by date/time
            cars[var] = pd.to_datetime(cars[var])
            cars = cars.sort_values(var)

            # Create a Streamlit slider for adjusting the time window of the plot
            max_time = cars[var].max()
            min_time = cars[var].min()

            if location == "newyork":
                minslider = min_time.to_pydatetime()
                maxslider = max_time.to_pydatetime()
            elif location == "austin":
                maxslider = max_time
                minslider = min_time

            default_time_range = ((minslider + timedelta(days=60)), (maxslider - timedelta(days=60)))
            selected_time_range = st.slider('Select a time range', min_value=minslider,
                                                    max_value=maxslider, value=default_time_range)

            # Filter the data by the selected time range
            cars = cars.loc[(cars[var] >= pd.to_datetime(selected_time_range[0])) & (
                        cars[var] <= pd.to_datetime(selected_time_range[1]))]

            # Set the index to the timestamp column
            cars = cars.set_index(var)

            # Plot the car1 and car2 columns over time
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=cars.index, y=cars['car1'], name='Car 1'))
            fig.add_trace(go.Scatter(x=cars.index, y=cars['car2'], name='Car 2'))
            fig.update_layout(title='Power consumption regarding EVs for building {}'.format(selected_building),
                            xaxis_title='Time', yaxis_title='Power (kW)')
            st.plotly_chart(fig, use_container_width=True)
