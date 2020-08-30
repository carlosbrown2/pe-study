import pandas as pd
from numpy import NaN
import numpy as np

df_saddle = pd.read_excel('PE Study- Final for Mayya 10_10_19.xlsx', sheet_name='Saddle PE')
df_nosaddle = pd.read_excel('PE Study- Final for Mayya 10_10_19.xlsx', sheet_name='Non-Saddle PE')

# Data Cleaning

# Rename columns
df_nosaddle.rename(columns={'Required supplemental O2':'Required Supplemental O2', 'Shock (BP <90)':'Shock (SBP <90)', 'tpA ':'tpA', 'Indentificaton':'ID', 'Hight-cm':'Height_cm'}, inplace=True)
df_saddle.rename(columns={' EKOS':'EKOS', 'tpA ':'tpA','Indentificaton':'ID', 'Hight-cm':'Height_cm'}, inplace=True)

# Replace 'x' with more data friendly missing value
def replacex(item):
    if str(item) == 'x':
        return NaN
    else:
        return item
        
# Clean datasets
saddle_cols = list(df_saddle.columns)
nosaddle_cols = list(df_nosaddle.columns)

for col in saddle_cols:
    df_saddle[col] = df_saddle[col].apply(replacex)
for col in nosaddle_cols:
    df_nosaddle[col] = df_nosaddle[col].apply(replacex)

# Remove whitespace from text borders
def strip_text(item):
    return item.strip()
df_saddle['Patient Status at 30 days'] = df_saddle['Patient Status at 30 days'].apply(strip_text)
df_nosaddle['Patient Status at 30 days'] = df_nosaddle['Patient Status at 30 days'].apply(strip_text)

# Generate Adverse Events Variable
# Variables that qualify as adverse event include death, Arrhythmia needing treatment, Supplemental O2 required, Ionotropes, Vasopressors
def adverse_event(row):
    adverse_event = 0
    if row['Patient Status at 30 days'] == 'Deceased' or row['Arrhythmia'] == 1 or row['Inotropes'] == 1 or row['Pressors'] == 1 or row["NRB (non-rebreather mask required)"] == 1 or row['ICU Stay'] == 1 or row['Shock (SBP <90)'] == 1 or row['ACLS'] == 1 or row['Intubation'] == 1 or row['tpA'] == 1 or row['Transfusion'] == 1 or row['EKOS'] == 1:
        adverse_event = 1
    return adverse_event
df_saddle['adverseEvent'] = df_saddle.apply(lambda row: adverse_event(row), axis=1)
df_nosaddle['adverseEvent'] = df_nosaddle.apply(lambda row: adverse_event(row), axis=1)

# Save clean data
df_saddle.to_csv('saddle.csv', index=False)
df_nosaddle.to_csv('nosaddle.csv', index=False)
print('Files Successfully Saved...')

