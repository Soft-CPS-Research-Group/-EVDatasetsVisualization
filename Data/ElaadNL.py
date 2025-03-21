import streamlit as st

class ElaadNL:

    def __str__(self):
        return "ElaadNL Open Datasets for Electric Mobility Research"

    @staticmethod
    def page():
        st.write("You have selected the ElaadNL Open Datasets for Electric Mobility Research dataset")
        link = "https://platform.elaad.io/analyses/index.php?url=ElaadNL_opendata.php"
        st.write("Data visualization is already done at the datasets' website")
        text = "Click here to go to dataset website. Use the word 'open' to access the dataset."
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

