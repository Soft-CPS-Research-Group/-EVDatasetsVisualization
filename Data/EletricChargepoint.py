import streamlit as st

class EletricChargepoint:

    def __str__(self):
        return "Electric Chargepoint Analysis 2017 Domestics"

    @staticmethod
    def page():
        st.write("You have selected the Electric Chargepoint Analysis 2017 Domestics dataset")
        st.write("A complete Data visualization and report is already done at the datasets' website")
        link = "https://www.gov.uk/government/statistics/electric-chargepoint-analysis-2017-domestics"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

