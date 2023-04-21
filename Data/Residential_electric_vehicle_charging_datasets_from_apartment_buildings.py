import streamlit as st
import pandas as pd
def page():
    st.write("You have selected the Residential electric vehicle charging datasets from apartment buildings dataset")
    link = "https://data.mendeley.com/datasets/jbks2rcwyj/2"
    text = "Click here to go to dataset website"
    st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

#selected_file = st.selectbox(
#    'Select the file that you want to visualize',
#    ("", ""))

# @st.cache_data
# def load_data():
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache_data)")
#
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
#
# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)
#
# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#
# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)