import streamlit as st

def page():
    st.write("You have selected the ElaadNL Open Datasets for Electric Mobility Research dataset")
    link = "https://platform.elaad.io/analyses/index.php?url=ElaadNL_opendata.php"
    text = "Click here to go to dataset website. Use the word 'open' to access the dataset"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

