import streamlit as st

def page():
    st.write("You have selected the City of Palo Alto - Perth & Kinross Council's Electric Vehicle Charging Station Usage dataset")
    link = "https://data.cityofpaloalto.org/dataviews/257812/ELECT-VEHIC-CHARG-STATI-83602/"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

