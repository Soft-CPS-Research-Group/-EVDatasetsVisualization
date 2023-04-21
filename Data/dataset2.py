import streamlit as st

def page():
    st.write("You have selected the Georgia Tech EV Campus Electric Vehicle Charging Stations Behavior dataset")
    link = "https://www.kaggle.com/datasets/claytonmiller/campus-electric-vehicle-charging-stations-behavior?select=Campus+EV+Charging+Behavior+Study.pdf"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

