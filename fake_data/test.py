import pandas as pd 

df = pd.read_csv('fake_data/CostReport_2019_Final.csv')
df_ny = df[df['State Code'] == 'NY']
df_ny = df_ny[df_ny['County'].isin(['SUFFOLK', 'NASSAU'])]
df_ny = df_ny.dropna(subset=['Medicaid Charges'])

list(df_ny.columns)

df_ny = df_ny[[
    'Hospital Name', 'Rural Versus Urban', 'Zip Code',
    'Number of Beds', 
    'Outpatient Revenue', 'Inpatient Revenue', 
    'Net Income', 'Medicaid Charges']]

df_ny['Rural Versus Urban'] = df_ny['Rural Versus Urban'].replace({'R': 'Rural', 'U': 'Urban'})

df_ny.to_csv('fake_data/ny_suffolk_nassau.csv', index=False)