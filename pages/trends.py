import pandas as pd
import random
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from dateutil import parser

import json


sehuba = pd.read_csv(r'C:\Users\BolokangMpoma\Documents\Streamlit\learn streamlit\flu_raw.csv')

#print(sehuba)

# Streamlit app for visualization

# Sidebar filters
st.sidebar.header("Please Filter Here:")
selected_gender = st.sidebar.multiselect(
    "Select Gender:",
    options=sehuba['Gender'].unique(),
    default=sehuba['Gender'].unique()
)

selected_district = st.sidebar.multiselect(
    "Select Districts:",
    options=sehuba['District'].unique(),
    default=sehuba['District'].unique()
)

# Apply filters
sehuba_selection = sehuba[
    (sehuba['Gender'].isin(selected_gender)) &
    (sehuba['District'].isin(selected_district))
]

# Check if the dataframe is empty
if sehuba_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()


    st.stop()



sehuba['Visit Date'] = sehuba['Visit Date'].apply(parser.parse)



# Group by Clinic Name and Quarter
clinic_quarter_visits = sehuba.groupby(['Clinic Name', 'Quarter']).size().unstack(fill_value=0)

# Group by Month
sehuba['Month'] = sehuba['Visit Date'].dt.month
monthly_visits = sehuba.groupby('Month').size()

# Group by Quarter
quarterly_visits = sehuba.groupby('Quarter').size()

# Monthly Visits Line Graph
#st.header("Monthly Visits")
fig, ax = plt.subplots()
monthly_visits.plot(kind='line', marker='o', ax=ax)
ax.set_xlabel('Month')
ax.set_ylabel('Number of Visits')
ax.set_title('Monthly Visits')
ax.set_xticks(range(1, 13))  # Ensure all months are shown
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.set_facecolor('#e6ffff')  # Light gray background
st.pyplot(fig)

# Quarterly Visits
#st.header("Quarterly Visits")
fig, ax = plt.subplots()
quarterly_visits.plot(kind='line', ax=ax)
ax.set_xlabel('Quarter')
ax.set_ylabel('Number of Visits')
ax.set_title('Quarterly Visits')
ax.set_facecolor('#e6ffff')  # Light gray background
st.pyplot(fig)