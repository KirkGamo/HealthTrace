import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Merging air quality and vegetation features with disease data...\n")

# Load the new features
airqual_veg = pd.read_csv(os.path.join(project_root, 'app/data/iloilo_airqual_vegetation.csv'))
airqual_veg['date'] = pd.to_datetime(airqual_veg['date'])
print(f"Air quality + vegetation records: {len(airqual_veg)}")
print(f"Date range: {airqual_veg['date'].min()} to {airqual_veg['date'].max()}")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    print(f"\n{'='*60}")
    print(f"Processing {disease.upper()}")
    print('='*60)
    
    # Load current atmosphere-enhanced data
    input_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Original data: {len(df)} records, {len(df.columns)} columns")
    print(f"Current features: {df.columns.tolist()}")
    
    # Merge with air quality and vegetation data
    df_merged = df.merge(airqual_veg, on='date', how='left')
    
    # New features to add
    new_features = ['no2', 'co', 'so2', 'o3', 'pm10', 'pm25', 'ndvi']
    
    print(f"\nAdding {len(new_features)} environmental features:")
    for feat in new_features:
        print(f"  - {feat}")
    
    # Fill any missing values
    for feat in new_features:
        if df_merged[feat].isna().sum() > 0:
            print(f"\nWarning: {feat} has {df_merged[feat].isna().sum()} missing values - forward filling")
            df_merged[feat] = df_merged[feat].ffill().bfill()
    
    print(f"\nMerged data: {len(df_merged)} records, {len(df_merged.columns)} columns")
    
    # Save the enhanced data with air quality and vegetation features
    output_file = os.path.join(project_root, f'app/data/{disease}_historical_data_full.csv')
    df_merged.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    
    # Show sample
    print(f"\nSample data:")
    print(df_merged[['date', 'disease_cases', 'tave', 'pm25', 'ndvi']].head())
    
    print(f"\nStatistics for new features:")
    print(df_merged[new_features].describe())

print(f"\n{'='*60}")
print("SUMMARY")
print('='*60)
print(f"✓ Added 7 environmental features to all 3 diseases")
print(f"  Air Quality (6): no2, co, so2, o3, pm10, pm25")
print(f"  Vegetation (1): ndvi")
print(f"  Previous features: 16")
print(f"  Total features now: 23 (input features)")
print(f"\nFiles created:")
for disease in diseases:
    print(f"  - app/data/{disease}_historical_data_full.csv")
