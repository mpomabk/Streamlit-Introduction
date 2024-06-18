import pandas as pd
import random
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import json


sehuba = pd.read_csv(r'C:\Users\BolokangMpoma\Documents\Streamlit\learn streamlit\flu_raw.csv')



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



# AGYW Calculation
agyw_count = sehuba[(sehuba['Patient Age'] >= 0) & (sehuba['Patient Age'] <= 23)].shape[0]
agyw_target = 250


# Total Visits Calculation
total_visits = sehuba['Patient_ID'].nunique()
total_visits_target = 2500

# Streamlit app
st.title("Progress to Targets")


# AGYW Progress Bar
st.header("AGYW Progress")
agyw_progress = agyw_count / agyw_target
st.progress(agyw_progress)
st.write(f"AGYW Count: {agyw_count} / {agyw_target} ({agyw_progress * 100:.2f}%)")


# Total Visits Progress Bar
st.header("Total Visits Progress")
total_visits_progress = total_visits / total_visits_target
st.progress(total_visits_progress)
st.write(f"Total Visits: {total_visits} / {total_visits_target} ({total_visits_progress * 100:.2f}%)")



# Group by Clinic Name and Quarter
clinic_quarter_visits = sehuba.groupby(['Clinic Name', 'Quarter']).size().unstack(fill_value=0)

# Get top 5 clinics by total visits
top_5_clinics = clinic_quarter_visits.sum(axis=1).nlargest(5).index

# Filter the data to include only the top 5 clinics
top_5_clinic_data = clinic_quarter_visits.loc[top_5_clinics]


# Top 5 Clinics Visits Over Quarters
fig, ax = plt.subplots()
top_5_clinic_data.T.plot(kind='bar', ax=ax)
ax.set_xlabel('Quarter')
ax.set_ylabel('Number of Visits')
ax.set_title('Top 5 Clinics Visits')
st.pyplot(fig)