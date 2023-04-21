import streamlit as st

def page():
    st.write("You have selected the Electric Chargepoint Analysis 2017 Domestics dataset")
    link = "https://www.gov.uk/government/statistics/electric-chargepoint-analysis-2017-domestics"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

