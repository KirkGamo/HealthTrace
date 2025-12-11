import pandas as pd

# Check Leptospirosis data
df = pd.read_csv('app/data/disease_pidsr_totals.csv')
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
