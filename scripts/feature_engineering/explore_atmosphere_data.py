import pandas as pd

# Load the climate atmosphere data
print("Loading climate_atmosphere_downscaled.csv...")
df = pd.read_csv('app/data/climate_atmosphere_downscaled.csv')

print(f"\nDataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())

# Filter for Iloilo City
if 'adm3_pcode' in df.columns:
    iloilo_data = df[df['adm3_pcode'] == 'PH063022000']
    print(f"\nIloilo City records: {len(iloilo_data)}")
    print(f"\nDate range: {iloilo_data['date'].min()} to {iloilo_data['date'].max()}")
    
    # Show available features
    numeric_cols = iloilo_data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    print(f"\nAvailable numeric features ({len(numeric_cols)}):")
    for col in numeric_cols:
        print(f"  - {col}")
