import streamlit as st

def page():
    st.write("You have selected the Energy consumption and renewable generation data of 5 aggregators dataset")
    link = "https://zenodo.org/record/4399670#.ZEJ07fzMK3A"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

