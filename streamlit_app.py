import streamlit as st
from PIL import Image
import base64

st.set_page_config(
    page_title="EV Data Visualization",
    page_icon="🚗",
    initial_sidebar_state="auto",
    menu_items=None,
)


from Data import (OBEV, PecanStreetviz, Residential_electric_vehicle_charging_datasets_from_apartment_buildings, GeorgiaTechEV,
                  Energy_consumption_and_renewable_generation_data_of_5_aggregators, PerthKinross, Boulder, Dundee,
                  EletricChargepoint, ElaadNL, PaloAlto, ACN_Data, ICharging, InitialPage, DOE)

st.markdown("""
<style>
.centered {
    display: block;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)



st.markdown("<h1 class='centered'>EVs' Datasets Data Visualization</h1>", unsafe_allow_html=True)

# Load your images (local file paths or URLs)
image1_path = "./Data/Images/logo-opeva.jpg"
image2_path = "./Data/Images/2023_logo.png"

# Load images using PIL
image1 = Image.open(image1_path)
image2 = Image.open(image2_path)

# Determine the smaller dimensions of the two images
width = min(image1.width, image2.width)
height = min(image1.height, image2.height)

# Resize the images to the smaller dimensions
image1_resized = image1.resize((width, height))
image2_resized = image2.resize((width, height))

logoOpeva = InitialPage.show_logo("https://opeva.eu/", image1_path,
        width=80, padding=[0, 0, 0, 0], margin=[0, 0, 0, 0]
    )
logoisep = InitialPage.show_logo("https://www.isep.ipp.pt/", image2_path,
        width=105, padding=[0, 0, 0, 0], margin=[0, 0, 0, 0]
    )

# Create two columns and add a single container for centering
left_column, center_column, right_column = st.columns([1, 2, 1])
with center_column:
    # Create two columns for images
    col1, col2 = st.columns(2)

    # Display images side by side
    col1.markdown(logoOpeva, unsafe_allow_html=True)
    col2.markdown(logoisep, unsafe_allow_html=True)

    #col1.image(image1_resized, use_column_width=True)
    #col2.image(image2_resized, use_column_width=True)

datasets = {
    "Initial Page": InitialPage.InitialPage(),
    "ACN Data": ACN_Data.ACN(),
    "Boulder Dataset": Boulder.Boulder(),
    "Dundee Dataset": Dundee.Dundee(),
    "ElaadNL Dataset": ElaadNL.ElaadNL(),
    "Electric Chargepoint": EletricChargepoint.EletricChargepoint(),
    "Five Aggregators": Energy_consumption_and_renewable_generation_data_of_5_aggregators.FiveAg(),
    "Georgia Tech EV": GeorgiaTechEV.GeorgiaTech(),
    "Palo Alto Dataset": PaloAlto.PaloAlto(),
    "Pecan Street": PecanStreetviz.Pecan(),
    "Perth Kinross": PerthKinross.PerthKinross(),
    "Apartment Charging": Residential_electric_vehicle_charging_datasets_from_apartment_buildings.REVC(),
    "Office building Dataset": OBEV.OBEV(),
    "DOE Dataset": DOE.DOE()
}

selected_name = st.selectbox("Please select the dataset you would like to visualize", list(datasets.keys()))

selected_dataset = datasets[selected_name]

selected_dataset.page()


st.write("________________________________________________________________________________________")

image3_path = "./Data/Images/EU.png"

# Create two columns and add a single container for centering
st.subheader("This work was funded by European Project:")

left1_column, right1_column = st.columns([3, 1])
with left1_column:
    link = "https://opeva.eu/"
    text = "OPEVA - OPtimization of Electric Vehicule Autonomy "
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)
    st.write("Funded by Key Digital Technologies Joint Undertaking (KDT JU) from the European Union’s Horizon Europe Programme and the National Authorities, under grant agreement 101097267.")
with right1_column:
    st.image(image3_path)

st.write("________________________________________________________________________________________")

left2_column, right2_column = st.columns([4, 2])
with left2_column:
    st.write("Created by: Tiago Fonseca")
    st.write("Co-Devloped by: Pedro Pires")
    st.write("Software for Cyber Physical Systems (SoftCPS) Research Group")
with right2_column:
    logo = InitialPage.show_logo("https://github.com/Soft-CPS-Research-Group/-EVDatasetsVisualization", "./Data/Images/128-1280187_github-logo-png-github-transparent-png.png",
        width=65, padding=[0, 6, 20, 25], margin=[0, 0, 30, 0]
    )
    st.markdown(logo, unsafe_allow_html=True)


