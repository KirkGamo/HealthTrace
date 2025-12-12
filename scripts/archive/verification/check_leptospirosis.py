import pandas as pd
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check Leptospirosis data
df = pd.read_csv(os.path.join(project_root, 'app/data/disease_pidsr_totals.csv'))
lep = df[df['disease_icd10_code'] == 'A27']
print(f'Total Leptospirosis records: {len(lep)}')

iloilo = lep[lep['adm3_pcode'] == 'PH063022000']
print(f'Iloilo City Leptospirosis records: {len(iloilo)}')
if len(iloilo) > 0:
    print(f'Date range: {iloilo["date"].min()} to {iloilo["date"].max()}')
    print(f'\nSample data:')
    print(iloilo.head())
else:
    print('No Leptospirosis data for Iloilo City')
