import streamlit as st
import pandas as pd

class REVC:

    def __str__(self):
        return "Residential electric vehicle charging datasets from apartment buildings"

    @staticmethod
    def page():
        st.write("You have selected the Residential electric vehicle charging datasets from apartment buildings dataset")
        st.write("Data visualization and analysis is already done at companion article")

        link = "https://www.sciencedirect.com/science/article/pii/S0378778821002073?via%3Dihub"
        text = "Click here to access it."
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)


        link = "https://data.mendeley.com/datasets/jbks2rcwyj/2"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

