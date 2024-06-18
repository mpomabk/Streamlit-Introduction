import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Number of records
num_records = 1000

# List of clinics in Botswana (based on the text provided)
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
    'Patient ID': [fake.uuid4() for _ in range(num_records)],
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

# Save the DataFrame to a CSV file
csv_file_path = 'flu_raw.csv'
df.to_csv(csv_file_path, index=False)

# Display the first few rows of the dataset
df.head()


clinics = pd.read_csv("data\CLINICS.csv")
clinics
#flu = df.merge(clinics, on='Patient ID', how='outer')
#flu