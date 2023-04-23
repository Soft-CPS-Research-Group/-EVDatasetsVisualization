import streamlit as st
import pandas as pd
def page():
    st.write("This EDA dashboard accompanies paper X Section 3.3. Please find more on the paper here")

    st.write("The dashboard provides a comprehensive guide and visualization to the latest open-source "
             "datasets related to EV's charging time series and charging flexibility behaviours. The dashboard "
             "quickly references the dataset URLs and also explores various metrics related to these datasets.")

    st.write("The following graphs and metrics are available on this dashboard for each dataset:")

    st.write(
        "- A histogram that shows the total number of charging hours per session.")

    st.write(
        "- A graph that shows the total number of charging sessions per amount of charging time, presented as two "
        "lines - one for weekdays and another for weekends")

    st.write(
        "- A graph that shows the number of charging sessions for each 15-minute interval of arriving and departing "
        "times, respectively, represented as a line graph.")

    st.write(
        "- A graph that shows the charging time  and the amount of energy charged during each session, "
        "with the X-axis binned in 15-minute intervals.")

    st.write("- A histogram of the energy supplied and the number of events that supplied that energy.")

    st.write("- Other metrics might apply given the specific data present at each dataset")