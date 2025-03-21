import streamlit as st
import pandas as pd
import plotly.express as px

class FiveAg:

    def __str__(self):
        return "Energy consumption and renewable generation data of 5 aggregators"

    @staticmethod
    def page():
        st.write("You have selected the Energy consumption and renewable generation data of 5 aggregators dataset")
        link = "https://zenodo.org/record/4399670#.ZEJ07fzMK3A"
        text = "Click here to go to dataset website"
        st.markdown(f"[{text}]({link})", unsafe_allow_html=True)

        # read the CSV file
        df = pd.read_csv('./Data/Energy consumption and renewable generation data of 5 aggregators/15min-Data_V7.csv',
                        sep=';', decimal=",")

        # Apply the fix_hour_format function to the DataFrame
        df = df.apply(fix_hour_format, axis=1)

        # Combine 'Days' and 'Time' columns and convert to datetime
        df['DateTime'] = pd.to_datetime(df['Days'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M')

        # Drop the original 'Days' and 'Time' columns
        df.drop(['Days', 'Time'], axis=1, inplace=True)

        # Create interactive line chart with Plotly
        fig = px.line(df, x="DateTime", y=["Slow1", "Slow2", "Fast1", "Fast2"],
                    labels={"value": "MW", "variable": "Lines"},
                    title="Interactive Line Graph for Slow and Fast Aggregators of EVs")

        # Show the interactive line chart in Streamlit
        st.plotly_chart(fig)



# Function to fix 24:00 hour format
def fix_hour_format(row):
    if row['Time'] == '24:00':
        row['Time'] = '00:00'
        row['Days'] = (pd.to_datetime(row['Days'], format='%d/%m/%Y') + pd.DateOffset(days=1)).strftime('%d/%m/%Y')
    return row    