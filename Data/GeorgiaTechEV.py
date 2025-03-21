import streamlit as st

class GeorgiaTech:

    def __str__(self):
        return "Georgia Tech EV Campus Electric Vehicle Charging Stations Behavior"

    @staticmethod
    def page():
        st.write("You have selected the Georgia Tech EV Campus Electric Vehicle Charging Stations Behavior dataset")
        st.write("Data visualization is already done at the datasets' website")
        link = "https://www.kaggle.com/datasets/claytonmiller/campus-electric-vehicle-charging-stations-behavior?select=Campus+EV+Charging+Behavior+Study.pdf"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

