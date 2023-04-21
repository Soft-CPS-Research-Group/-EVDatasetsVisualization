import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json
# Import the necessary plotly components
import plotly.graph_objs as go

def page():
    st.write("You have selected the ACN-Data dataset")
    link = "https://ev.caltech.edu/dataset"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

    site = st.selectbox("Select Site", ("caltech", "jpl", "office1"))

    with open("./Data/ACN-Data/" + site + ".json") as f:
        data = json.load(f)

    df = pd.json_normalize(data["_items"])

    # Display the raw data in a table
    st.write(df)

    # Display a histogram of kWhDelivered
    fig_kwh = px.histogram(df, x="kWhDelivered", nbins=20, title="kWh Delivered Distribution")
    st.plotly_chart(fig_kwh)

    # Display a bar chart of the number of charging sessions per spaceID
    space_counts = df["spaceID"].value_counts().reset_index()
    space_counts.columns = ["spaceID", "count"]
    fig_space = px.bar(space_counts, x="spaceID", y="count", title="Number of Charging Sessions per SpaceID")
    st.plotly_chart(fig_space)

    # Display a line chart of the connection and disconnect times
    df["connectionTime"] = pd.to_datetime(df["connectionTime"])
    df["disconnectTime"] = pd.to_datetime(df["disconnectTime"])

    # Extract the time part of the connectionTime and disconnectTime as timedelta
    df["connectionTime_td"] = df["connectionTime"].dt.time.apply(lambda t: pd.to_timedelta(t.strftime('%H:%M:%S')))
    df["disconnectTime_td"] = df["disconnectTime"].dt.time.apply(lambda t: pd.to_timedelta(t.strftime('%H:%M:%S')))

    # Bin the connection and disconnection times in 15-minute intervals
    bin_minutes = 15
    df["connectionTime_binned"] = bin_timedelta_data(df["connectionTime_td"], bin_minutes)
    df["disconnectTime_binned"] = bin_timedelta_data(df["disconnectTime_td"], bin_minutes)

    # Group the data by the binned connectionTime and disconnectTime, count the number of sessions, and sort the data
    grouped_conn_times = df.groupby("connectionTime_binned").size().reset_index(name="count").sort_values(
        "connectionTime_binned")
    grouped_disc_times = df.groupby("disconnectTime_binned").size().reset_index(name="count").sort_values(
        "disconnectTime_binned")

    # Convert the interval data to strings
    grouped_conn_times["connectionTime_binned"] = grouped_conn_times["connectionTime_binned"].apply(
        lambda x: f'{x.left} - {x.right}')
    grouped_disc_times["disconnectTime_binned"] = grouped_disc_times["disconnectTime_binned"].apply(
        lambda x: f'{x.left} - {x.right}')

    # Create a line chart with separate lines for connection times and disconnection times
    fig_times = go.Figure()
    fig_times.add_trace(
        go.Scatter(x=grouped_conn_times["connectionTime_binned"], y=grouped_conn_times["count"], mode='lines',
                   name='Connection Times'))
    fig_times.add_trace(
        go.Scatter(x=grouped_disc_times["disconnectTime_binned"], y=grouped_disc_times["count"], mode='lines',
                   name='Disconnection Times'))
    fig_times.update_layout(
        title=f'Number of Sessions by Connection and Disconnection Times (Binned in {bin_minutes}-minute intervals)',
        xaxis_title='Time', yaxis_title='Count')
    st.plotly_chart(fig_times)


# Define a function to bin timedelta data
def bin_timedelta_data(data, bin_minutes):
    bins = pd.timedelta_range(start='0 days', end='1 days', freq=f'{bin_minutes}T')
    binned_data = pd.cut(data, bins, right=False)
    return binned_data
