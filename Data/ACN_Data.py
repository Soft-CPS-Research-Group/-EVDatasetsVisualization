import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json

def page():
    st.write("You have selected the ACN-Data dataset")
    link = "https://ev.caltech.edu/dataset"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

    with open("./Data/ACN-Data/caltech.json") as f:
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
    df_times = df[["connectionTime", "disconnectTime"]].sort_values("connectionTime")
    fig_times = px.line(df_times, x="connectionTime", y="disconnectTime", title="Connection and Disconnect Times")
    st.plotly_chart(fig_times)