import pandas as pd
import random
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from faker import Faker
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize Faker
fake = Faker()

# Number of records
num_records = 1000

# List of clinics in Botswana
clinics = [
    "Block 9-Julia Molefhe Extension 2 Nkoyaphiri", "Gaborone west", "Broadhurst 3 (BH3)", "Mafitlhakgosi", "Lesirane", 
    "Old Naledi", "Gerald", "Tati Siding", "Tonota", "Jubilee", "Sesame", "Botshabelo", "Tapologong", "Boseja II", 
    "Bokaa", "Oodi", "Otse", "Moshupa", "Lerala", "Boipelego", "Peleng East", "Tsopeng", "Ditsweletse", "Phuthadikobo", 
    "Takatokwane", "Letlhakeng", "Sese", "Sebina", "Nata", "Kang", "Airstrip", "Shoshong", "Mopipi", "Mabutsane", 
    "Khakhea", "Charleshill", "Kachikau", "Mathethe", "Kanye Main Clinic", "Kgwatlheng", "Maun General Clinic", 
    "Moeti", "Shakawe"
]

# Generate data
data = {
    'Patient_ID': [fake.uuid4() for _ in range(num_records)],
    'Visit Date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_records)],
    'Clinic ID': [fake.random_int(min=1, max=len(clinics)) for _ in range(num_records)],
    'Clinic Name': [random.choice(clinics) for _ in range(num_records)],
    'Patient Age': [fake.random_int(min=0, max=100) for _ in range(num_records)],
    'Patient Gender': [random.choice(['Male', 'Female']) for _ in range(num_records)],
    'Symptoms': [random.choice(['fever', 'cough', 'sore throat', 'headache', 'fatigue']) for _ in range(num_records)],
    'Diagnosis': [random.choice(['flu', 'common cold', 'respiratory infection']) for _ in range(num_records)],
    'Treatment Given': [random.choice(['medication', 'rest', 'fluids']) for _ in range(num_records)],
    'Follow-up Required': [random.choice(['Yes', 'No']) for _ in range(num_records)],
}

# Create DataFrame
df = pd.DataFrame(data)

# Dictionary mapping clinic names to district names
clinic_to_district = {
    "Block 9-Julia Molefhe Extension 2 Nkoyaphiri": "South-East District",
    "Gaborone west": "South-East District",
    "Broadhurst 3 (BH3)": "South-East District",
    "Mafitlhakgosi": "Central District",
    "Lesirane": "North-East District",
    "Old Naledi": "South-East District",
    "Gerald": "North-East District",
    "Tati Siding": "North-East District",
    "Tonota": "Central District",
    "Jubilee": "South-East District",
    "Sesame": "Central District",
    "Botshabelo": "Central District",
    "Tapologong": "Central District",
    "Boseja II": "Central District",
    "Bokaa": "Central District",
    "Oodi": "South-East District",
    "Otse": "Kweneng District",
    "Moshupa": "Southern District",
    "Lerala": "Central District",
    "Boipelego": "Kweneng District",
    "Peleng East": "Central District",
    "Tsopeng": "Central District",
    "Ditsweletse": "Kweneng District",
    "Phuthadikobo": "Central District",
    "Takatokwane": "Central District",
    "Letlhakeng": "Kweneng District",
    "Sese": "Central District",
    "Sebina": "Central District",
    "Nata": "Central District",
    "Kang": "Central District",
    "Airstrip": "Central District",
    "Shoshong": "Central District",
    "Mopipi": "Ghanzi District",
    "Mabutsane": "Southern District",
    "Khakhea": "Ghanzi District",
    "Charleshill": "North-East District",
    "Kachikau": "North-West District",
    "Mathethe": "Southern District",
    "Kanye Main Clinic": "Southern District",
    "Kgwatlheng": "Kweneng District",
    "Maun General Clinic": "North-West District",
    "Moeti": "Ghanzi District",
    "Shakawe": "North-West District"
}

# Add a new column 'District' to the DataFrame
df['District'] = df['Clinic Name'].map(clinic_to_district)

# Add additional columns
df['Age'] = [fake.random_int(min=0, max=100) for _ in range(num_records)]
df['Gender'] = [random.choice(['Male', 'Female']) for _ in range(num_records)]
df['Pregnant'] = [random.choice(['Yes', 'No']) for _ in range(num_records)]

# List of COVID-19 vaccine names
covid_vaccines = ['Pfizer-BioNTech', 'Moderna', 'Johnson & Johnson', 'AstraZeneca', 'Sinovac', 'Sinopharm', 'Sputnik V', 'Covaxin']
df['Covid_Vaccine'] = [random.choice(covid_vaccines) for _ in range(num_records)]

df['Medical Aid'] = [random.choice(['Yes', 'No']) for _ in range(num_records)]

# Add a new column 'Job Type' to the DataFrame
job_types = ['farm worker', 'construction worker', 'office worker', 'health worker']
df['Job Type'] = [random.choice(job_types) for _ in range(num_records)]

# Add a new column 'Mode of Transport' to the DataFrame
modes_of_transport = ['private car', 'public transport', 'shared private car']
df['Mode of Transport'] = [random.choice(modes_of_transport) for _ in range(num_records)]


# Convert "Visit Date" to datetime format
df['Visit Date'] = pd.to_datetime(df['Visit Date'], format='%d %b %Y')

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
df['Quarter'] = df['Visit Date'].apply(get_quarter)





# Reorder the columns
df = df[['Patient_ID', 'Visit Date', 'Clinic ID', 'Clinic Name', 
         'District', 'Age', 'Gender', 'Pregnant', 'Covid_Vaccine', 
         'Medical Aid', 'Job Type', 'Mode of Transport', 
         'Patient Age', 'Patient Gender', 'Symptoms', 'Diagnosis', 
         'Treatment Given', 'Quarter','Follow-up Required']]

# Save the DataFrame to a CSV file
csv_file_path = 'flu_raw.csv'
df.to_csv(csv_file_path, index=False)

sehuba = df.copy()


# Streamlit app for visualization

# Sidebar filters
st.sidebar.header("Please Filter Here:")
selected_gender = st.sidebar.multiselect(
    "Select Gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

#selected_vaccine = st.sidebar.multiselect(
#    "Select Vaccine Status:",
#   options=df['Covid_Vaccine'].unique(),
 #   default=df['Covid_Vaccine'].unique()
#)

selected_district = st.sidebar.multiselect(
    "Select Districts:",
    options=df['District'].unique(),
    default=df['District'].unique()
)

# Apply filters
df_selection = df[
    (df['Gender'].isin(selected_gender)) &
    #(df['Covid_Vaccine'].isin(selected_vaccine)) &
    (df['District'].isin(selected_district))
]

# Check if the dataframe is empty
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

# Display filtered data
# st.dataframe(df_selection) # Commented out to not display the dataset


###trial

# Visualization: Age Distribution by Gender
fig1 = px.histogram(df_selection, x='Patient Age', color='Patient Gender', title='Age Distribution by Gender')
#st.plotly_chart(fig1)

# Visualization: Number of Visits per Clinic (Top 10)
visits_per_clinic = df_selection['Clinic Name'].value_counts().reset_index().head(5)
visits_per_clinic.columns = ['Clinic Name', 'Visit Count']
fig2 = px.bar(visits_per_clinic, x='Clinic Name', y='Visit Count', title='Top 10 Clinics by Number of Visits')
#st.plotly_chart(fig2)


# Visualization: Number of Visits per District (Top 10)
visits_per_district = df_selection['District'].value_counts().reset_index().head(5)
visits_per_district.columns = ['District', 'Visit Count']
fig3 = px.bar(visits_per_district, x='District', y='Visit Count', title='Top 10 Districts by Number of Visits')
#st.plotly_chart(fig3)

# New visualization for the total number of unique patients
total_unique_patients = df_selection['Patient_ID'].nunique()
st.markdown(f"**<span style='color:brown'>Total Unique Patients: {total_unique_patients}</span>**", unsafe_allow_html=True)

# Visualization: Common Symptoms by Gender
symptoms_by_gender = df_selection.groupby(['Symptoms', 'Patient Gender']).size().reset_index(name='Counts')
fig4 = px.bar(symptoms_by_gender, x='Symptoms', y='Counts', color='Patient Gender', barmode='group', title='Common Symptoms by Gender')
#st.plotly_chart(fig4)



# Place the visualizations side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.plotly_chart(fig3, use_container_width=True)





#Age Distribution next to Symptoms
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig4, use_container_width=True)



