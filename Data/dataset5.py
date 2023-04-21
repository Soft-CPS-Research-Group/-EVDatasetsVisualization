import streamlit as st

def page():
    st.write("You have selected the City of Boulder Electric Vehicle Charging Station Energy Consumption dataset")
    link = "https://open-data.bouldercolorado.gov/datasets/39288b03f8d54b39848a2df9f1c5fca2_0/about"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

