import streamlit as st

def page():
    st.write("You have selected the Electric Vehicle Charging Sessions Dundee dataset")
    link = "https://data.dundeecity.gov.uk/dataset/ev-charging-data"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

