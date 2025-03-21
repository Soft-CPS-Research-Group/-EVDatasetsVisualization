import streamlit as st
import pandas as pd
from PIL import Image
import base64

class InitialPage:

    def __str__(self):
        return "Initial Page"

    @staticmethod
    def page():


        st.write("This dashboard provides a comprehensive guide and visualization to the latest open-source datasets related to EV's charging time series and charging flexibility behaviours. The dashboard quickly references the dataset URLs and also explores various metrics related to these datasets.")
        #centered_text = "<div style='text-align: center;'>This dashboard provides a comprehensive guide and visualization to the latest open-source datasets related to EV's charging time series and charging flexibility behaviours. The dashboard quickly references the dataset URLs and also explores various metrics related to these datasets.</div>"
        #st.markdown(centered_text, unsafe_allow_html=True)

        st.write("This dashboard accompanies paper X Section 3.3. Please find more on the paper here")
        #centered_text = "<div style='text-align: center;'>This dashboard accompanies paper X Section 3.3. Please find more on the paper here</div>"
        #st.markdown(centered_text, unsafe_allow_html=True)

        st.write("")

        #st.write("The dashboard provides a comprehensive guide and visualization to the latest open-source "
        #         "datasets related to EV's charging time series and charging flexibility behaviours. The dashboard "
        #         "quickly references the dataset URLs and also explores various metrics related to these datasets.")

        #with st.expander("Learn More abou the dashboard:"):

        st.write("The following graphs and metrics may be available for each dataset:")

        st.write(
            "- A histogram that shows the total number of charging hours per session.")

        st.write(
            "- A graph that shows the total number of charging sessions per amount of charging time, presented as two "
            "lines - one for weekdays and another for weekends, or as a different graph for each day of the week")

        st.write(
            "- A graph that shows the number of charging sessions for each 15-minute interval of arriving and departing "
            "times, respectively, represented as a line graph.")

        st.write(
            "- A graph that shows the charging time  and the amount of energy charged during each session, "
            "with the X-axis binned in 15-minute intervals.")

        st.write("- A histogram of the energy supplied and the number of events that supplied that energy.")

        st.write("- Other metrics might apply given the specific data present at each dataset")

def show_logo(link, path, width, padding, margin):
        padding_top, padding_right, padding_bottom, padding_left = padding
        margin_top, margin_right, margin_bottom, margin_left = margin

        link = link

        with open(path, "rb") as f:
            data = f.read()

        bin_str = base64.b64encode(data).decode()
        html_code = f"""
            <a href="{link}" target = _blank>
                <img src="data:image/png;base64,{bin_str}"
                style="
                    margin: auto;
                    width: {width}%;
                    margin-top: {margin_top}px;
                    margin-right: {margin_right}px;
                    margin-bottom: {margin_bottom}px;
                    margin-left: {margin_left}%;
                    padding-top: {margin_top}px;
                    padding-right: {padding_right}px;
                    padding-bottom: {padding_bottom}px;
                    padding-left: {padding_left}%;
                    "/>
            </a>"""

        return html_code