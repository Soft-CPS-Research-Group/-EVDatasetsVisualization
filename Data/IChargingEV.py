import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class ICEV:
    def __str__(self):
        return "I-Charging"
    
    @staticmethod
    def page():
        st.write("You have selected the I-Charging EV dataset")