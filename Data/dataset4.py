import streamlit as st

def page():
    st.write("You have selected the Perth & Kinross Council's Perth & Kinross Council's Electric Vehicle Charging Station Usage dataset")
    link = "https://data.pkc.gov.uk/dataset/ev-charging-data"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

