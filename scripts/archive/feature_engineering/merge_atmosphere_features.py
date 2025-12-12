import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Merging atmosphere features with existing enhanced data...\n")

# Load the new climate atmosphere features
climate_atmos = pd.read_csv(os.path.join(project_root, 'app/data/iloilo_climate_atmosphere.csv'))
climate_atmos['date'] = pd.to_datetime(climate_atmos['date'])
print(f"Climate atmosphere records: {len(climate_atmos)}")
print(f"Date range: {climate_atmos['date'].min()} to {climate_atmos['date'].max()}")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    print(f"\n{'='*60}")
    print(f"Processing {disease.upper()}")
    print('='*60)
    
    # Load existing enhanced data
    input_file = os.path.join(project_root, f'app/data/{disease}_historical_data_enhanced.csv')
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Original data: {len(df)} records, {len(df.columns)} columns")
    print(f"Columns: {df.columns.tolist()}")
    
    # Merge with atmosphere data
    df_merged = df.merge(climate_atmos, on='date', how='left')
    
    # Select the atmosphere features we want to add
    # Note: 'pr' (precipitation) already exists in our data, so we'll skip it
    new_features = ['tmin', 'tmax', 'tave', 'temp_range', 'tave_7day', 'tave_30day']
    
    print(f"\nAdding {len(new_features)} temperature features:")
    for feat in new_features:
        print(f"  - {feat}")
    
    # Fill any missing values
    for feat in new_features:
        if df_merged[feat].isna().sum() > 0:
            print(f"\nWarning: {feat} has {df_merged[feat].isna().sum()} missing values - forward filling")
            df_merged[feat] = df_merged[feat].ffill().bfill()
    
    print(f"\nMerged data: {len(df_merged)} records, {len(df_merged.columns)} columns")
    
    # Save the enhanced data with atmosphere features
    output_file = os.path.join(project_root, f'app/data/{disease}_historical_data_atmosphere.csv')
    df_merged.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    
    # Show sample
    print(f"\nSample data:")
    print(df_merged[['date', 'disease_cases', 'tmin', 'tmax', 'tave', 'temp_range']].head())
    
    print(f"\nStatistics for new features:")
    print(df_merged[new_features].describe())

print(f"\n{'='*60}")
print("SUMMARY")
print('='*60)
print(f"✓ Added 6 temperature features to all 3 diseases")
print(f"  Features: tmin, tmax, tave, temp_range, tave_7day, tave_30day")
print(f"  Total features now: {len(df_merged.columns) - 1} (excluding date)")
print(f"\nFiles created:")
for disease in diseases:
    print(f"  - app/data/{disease}_historical_data_atmosphere.csv")
