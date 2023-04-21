import streamlit as st
import pandas as pd
import numpy as np
import os

from Data import (PecanStreetviz, Residential_electric_vehicle_charging_datasets_from_apartment_buildings, dataset2,
                  Energy_consumption_and_renewable_generation_data_of_5_aggregators, dataset4, dataset5, dataset6,
                  dataset7, dataset8, dataset9, ACN_Data, ICharging)


st.title('EV Datasets Analysis')

# specify the path of the directory
directory_path = './Data'

# get a list of all files and directories in the directory
dir_contents = os.listdir(directory_path)

# filter out only the directories
directories = [dir_name for dir_name in dir_contents if os.path.isdir(os.path.join(directory_path, dir_name))]

selected_dataset = st.selectbox(
    'Please select the dataset that you would like to visualize',
    directories)

if selected_dataset == "Residential electric vehicle charging datasets from apartment buildings":
    Residential_electric_vehicle_charging_datasets_from_apartment_buildings.page()
elif selected_dataset == "Georgia Tech EV Campus Electric Vehicle Charging Stations Behavior":
    dataset2.page()
elif selected_dataset == "Energy consumption and renewable generation data of 5 aggregators":
    Energy_consumption_and_renewable_generation_data_of_5_aggregators.page()
elif selected_dataset == "Perth & Kinross Council's Electric Vehicle Charging Station Usage":
    dataset4.page()
elif selected_dataset == "City of Boulder Electric Vehicle Charging Station Energy Consumption":
    dataset5.page()
elif selected_dataset == "Electric Vehicle Charging Sessions Dundee":
    dataset6.page()
elif selected_dataset == "Electric Chargepoint Analysis 2017 Domestics":
    dataset7.page()
elif selected_dataset == "ElaadNL Open Datasets for Electric Mobility Research":
    dataset8.page()
elif selected_dataset == "City of Palo Alto - Electric Vehicle Charging Station Usage":
    dataset9.page()
elif selected_dataset == "ACN-Data":
    ACN_Data.page()
elif selected_dataset == "PecanStreet":
    PecanStreetviz.page()
elif selected_dataset == "ICharging":
    ICharging.page()
else:
    st.error("The dataset you selected could not be found on our database")

