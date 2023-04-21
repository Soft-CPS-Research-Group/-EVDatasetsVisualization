import streamlit as st

def page():
    st.write("You have selected the ACN-Data dataset")
    link = "https://ev.caltech.edu/dataset"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

