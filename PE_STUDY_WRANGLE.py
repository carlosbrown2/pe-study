import pandas as pd
from numpy import NaN
import numpy as np

df_saddle = pd.read_csv('./objects/Saddle PE-Table 1.csv')
df_nosaddle = pd.read_csv('./objects/Non-Saddle PE-Table 1.csv')

# Data Cleaning
# Rename columns
df_nosaddle.rename(columns={' EKOS':'EKOS', 
                            'tpA ':'tpA',
                            'Indentificaton':'ID', 
                            'Hight-cm':'Height_cm', 
                            'sPESI (low risk = 0; 1 = 1 or greater)':'sPESI'}, 
                            inplace=True)
df_saddle.rename(columns={' EKOS':'EKOS', 
                        'tpA ':'tpA',
                        'Indentificaton':'ID', 
                        'Hight-cm':'Height_cm', 
                        'sPESI (low risk = 0; 1 = 1 or greater)':'sPESI', 
                        'Shock (SBP <90)':'Shock (BP <90)',
                        'PE Severity 1=low risk; 2=intermediate; 3=massive; 4= indeterminate':'PE Severity 1=low risk; 2=intermediate; 3=massive; 4=indeterminate'}, 
                        inplace=True)

# Remove whitespace from text borders
def strip_text(item):
    return str(item).strip()

# Replace 'x' with more data friendly missing value
def replacesymbol(item):
    if str(item).strip() == 'x' or str(item).strip() == '?':
        return np.nan
    else:
        return item
        
# Clean datasets
saddle_cols = list(df_saddle.columns)
nosaddle_cols = list(df_nosaddle.columns)

for col in saddle_cols:
    df_saddle[col] = df_saddle[col].apply(replacesymbol)
for col in nosaddle_cols:
    df_nosaddle[col] = df_nosaddle[col].apply(replacesymbol)

# df_saddle['Patient Status at 30 days'] = df_saddle['Patient Status at 30 days'].apply(strip_text)
# df_nosaddle['Patient Status at 30 days'] = df_nosaddle['Patient Status at 30 days'].apply(strip_text)

# Generate Adverse Events Variable
# Variables that qualify as adverse event include death, Arrhythmia needing treatment, Supplemental O2 required, Ionotropes, Vasopressors
def adverse_event(row):
    adverse_event = 0
    if row['Death- In Hospital'] == 1 or row['Death within 30 days of discharge'] == 1 or \
        row['Arrhythmia that required treatment'] == 1 or row['Inotropes'] == 1 or \
        row['Pressors'] == 1 or row["NRB (non-rebreather mask required)"] == 1 or \
        row['Shock (BP <90)'] == 1 or row['ACLS'] == 1 or \
        row['Intubation'] == 1 or row['tpA'] == 1 or row['Transfusion'] == 1 or \
        row['EKOS'] == 1:
        adverse_event = 1
    return adverse_event
df_saddle['adverseEvent'] = df_saddle.apply(lambda row: adverse_event(row), axis=1)
df_nosaddle['adverseEvent'] = df_nosaddle.apply(lambda row: adverse_event(row), axis=1)

# Combine Dataframes
df_saddle['type'] = 'saddle'
df_nosaddle['type'] = 'non-saddle'
print(df_saddle.head())
df_saddle = df_saddle.drop(columns=['ID']).reset_index(drop=True)
df_nosaddle = df_nosaddle.drop(columns=['ID']).reset_index(drop=True)
print(df_saddle.head())
df_all = pd.concat([df_saddle, df_nosaddle], ignore_index=True)

# Save clean data
df_all.to_csv('./objects/all_types.csv', index=False)
print('File Successfully Saved...')

