import pandas as pd
import random
import streamlit as st
import plotly.express as px
from dateutil import parser
import json


sehuba = pd.read_csv(r'C:\Users\BolokangMpoma\Documents\Streamlit\learn streamlit\flu_raw.csv')


# Convert "Visit Date" to datetime format
sehuba['Visit Date'] = pd.to_datetime(sehuba['Visit Date'], format='%d %b %Y')

# Define a function to map the date to the appropriate quarter
def get_quarter(date):
    month = date.month
    if month in [10, 11, 12]:
        return 'Q1'
    elif month in [1, 2, 3]:
        return 'Q2'
    elif month in [4, 5, 6]:
        return 'Q3'
    else:  # 7, 8, 9
        return 'Q4'

# Apply the function to create a new "Quarter" column
sehuba['Quarter'] = sehuba['Visit Date'].apply(get_quarter)



# Coordinates for some districts in Botswana
district_coordinates = {
    "South-East District": {'lat': -24.658, 'lon': 25.908},
    "Central District": {'lat': -22.528, 'lon': 26.857},
    "North-East District": {'lat': -20.897, 'lon': 27.520},
    "Kweneng District": {'lat': -23.192, 'lon': 25.257},
    "Southern District": {'lat': -25.355, 'lon': 25.595},
    "Ghanzi District": {'lat': -21.699, 'lon': 21.665},
    "North-West District": {'lat': -19.417, 'lon': 22.209}
}

# Add latitude and longitude columns to the DataFrame
sehuba['Latitude'] = sehuba['District'].map(lambda x: district_coordinates.get(x, {}).get('lat'))
sehuba['Longitude'] = sehuba['District'].map(lambda x: district_coordinates.get(x, {}).get('lon'))
sehuba['Visit Date'] = sehuba['Visit Date'].apply(parser.parse)
# Reorder the columns
sehuba = sehuba[['Patient_ID', 'Visit Date', 'Clinic ID', 'Clinic Name', 'District', 'Latitude', 'Longitude', 'Patient Age', 'Patient Gender', 
         'Gender', 'Pregnant', 'Covid_Vaccine', 'Medical Aid', 'Job Type', 'Mode of Transport', 'Symptoms', 
         'Diagnosis', 'Treatment Given', 'Quarter', 'Follow-up Required']]

# Save the DataFrame to a CSV file
csv_file_path = 'flu_raw.csv'
sehuba.to_csv(csv_file_path, index=False)


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


st.title("TOP PERFROMING DISTRICTS")


# Identify top 5 districts by number of visits
top_districts = sehuba_selection['District'].value_counts().head(5).index.tolist()

# Visualization: Map of Clinic Distribution
sehuba_selection['Top District'] = sehuba_selection['District'].apply(lambda x: 'Top 5' if x in top_districts else 'Other')

# Count visits per clinic for marker size
visits_per_clinic = sehuba_selection.groupby('Clinic Name').size().reset_index(name='Visit Count')

# Merge visit counts with selection
sehuba_selection = sehuba_selection.merge(visits_per_clinic, on='Clinic Name', how='left')

# Create the map
fig_map = px.scatter_mapbox(
    sehuba_selection,
    lat="Latitude",
    lon="Longitude",
    hover_name="Clinic Name",
    hover_data={
        "District": True,
        "Clinic ID": True,
        "Visit Count": True,
        "Latitude": False,
        "Longitude": False
    },
    color="Top District",
    size="Visit Count",
    size_max=15,
    zoom=5,
    height=600,
    title="Clinic Distribution across Districts in Botswana (Top 5 Districts Highlighted)"
)

# Mapbox token (replace 'your_mapbox_token_here' with your actual Mapbox token)
px.set_mapbox_access_token('your_mapbox_token_here')

fig_map.update_layout(
    mapbox_style="open-street-map",
    legend_title_text='District Category',
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig_map, use_container_width=True)

# Visualization: Age Distribution by Gender
fig1 = px.histogram(sehuba_selection, x='Patient Age', color='Patient Gender', title='Age Distribution by Gender')
