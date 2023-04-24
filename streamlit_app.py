import streamlit as st

st.set_page_config(
    page_title="EV EDA",
    page_icon="🚗",
    initial_sidebar_state="auto",
    menu_items=None,
)


from Data import (PecanStreetviz, Residential_electric_vehicle_charging_datasets_from_apartment_buildings, GeorgiaTechEV,
                  Energy_consumption_and_renewable_generation_data_of_5_aggregators, dataset4, Boulder, Dundee,
                  EletricChargepoint, ElaadNL, PaloAlto, ACN_Data, ICharging, InitialPage)


st.title("EVs' Datasets Exploratory Data Analysis 🚗🔋⚡🔌")


# specify the path of the directory
directory_path = './Data'

# filter out only the directories
directories = ['Initial Page', 'ACN-Data', 'City of Boulder Electric Vehicle Charging Station Energy Consumption', 'City of Palo Alto - Electric Vehicle Charging Station Usage',
               'Electric Chargepoint Analysis 2017 Domestics', 'Electric Vehicle Charging Sessions Dundee', 'Energy consumption and renewable generation data of 5 aggregators',
               'Georgia Tech EV Campus Electric Vehicle Charging Stations Behavior', 'ICharging', 'PecanStreet', "Perth & Kinross Council's Electric Vehicle Charging Station Usage",
               'Residential electric vehicle charging datasets from apartment buildings', "ElaadNL Open Datasets for Electric Mobility Research"]

selected_dataset = st.selectbox(
    'Please select the dataset that you would like to visualize',
    directories, index=0)

if selected_dataset == "Initial Page":
    InitialPage.page()
elif selected_dataset == "Residential electric vehicle charging datasets from apartment buildings":
    Residential_electric_vehicle_charging_datasets_from_apartment_buildings.page()
elif selected_dataset == "Georgia Tech EV Campus Electric Vehicle Charging Stations Behavior":
    GeorgiaTechEV.page()
elif selected_dataset == "Energy consumption and renewable generation data of 5 aggregators":
    Energy_consumption_and_renewable_generation_data_of_5_aggregators.page()
elif selected_dataset == "Perth & Kinross Council's Electric Vehicle Charging Station Usage":
    dataset4.page()
elif selected_dataset == "City of Boulder Electric Vehicle Charging Station Energy Consumption":
    Boulder.page()
elif selected_dataset == "Electric Vehicle Charging Sessions Dundee":
    Dundee.page()
elif selected_dataset == "Electric Chargepoint Analysis 2017 Domestics":
    EletricChargepoint.page()
elif selected_dataset == "ElaadNL Open Datasets for Electric Mobility Research":
    ElaadNL.page()
elif selected_dataset == "City of Palo Alto - Electric Vehicle Charging Station Usage":
    PaloAlto.page()
elif selected_dataset == "ACN-Data":
    ACN_Data.page()
elif selected_dataset == "PecanStreet":
    PecanStreetviz.page()
elif selected_dataset == "ICharging":
    ICharging.page()
else:
    st.error("The dataset you selected could not be found on our database")





