import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Extracting Healthcare and Wealth Index features for Iloilo City...\n")

# Load location data to get Iloilo City barangays
print("Loading location data...")
location_df = pd.read_csv(os.path.join(project_root, 'app/data/location.csv'))
iloilo_brgys = location_df[location_df['adm3_pcode'] == 'PH063022000']['adm4_pcode'].tolist()
iloilo_brgys_set = set(iloilo_brgys)
print(f"Found {len(iloilo_brgys)} barangays in Iloilo City")

# ==================== HEALTHCARE ====================
print("\n" + "="*60)
print("EXTRACTING HEALTHCARE FEATURES")
print("="*60)

print("\nLoading osm_poi_health.csv...")
health_df = pd.read_csv(os.path.join(project_root, 'app/data/osm_poi_health.csv'))

# Filter for Iloilo City barangays
print("Filtering for Iloilo City...")
iloilo_health = health_df[health_df['adm4_pcode'].isin(iloilo_brgys_set)].copy()
print(f"Iloilo City healthcare records: {len(iloilo_health)}")

# Convert date
iloilo_health['date'] = pd.to_datetime(iloilo_health['date'])

# Select key healthcare features (count and nearest distance)
healthcare_features = {
    'clinic_count': 'mean',
    'clinic_nearest': 'mean',
    'hospital_count': 'mean',
    'hospital_nearest': 'mean',
    'pharmacy_count': 'mean',
    'pharmacy_nearest': 'mean',
    'doctors_count': 'mean',
    'doctors_nearest': 'mean',
}

print("\nAggregating healthcare data by date...")
daily_health = iloilo_health.groupby('date').agg(healthcare_features).reset_index()

print(f"\nAggregated healthcare records: {len(daily_health)}")
print(f"Date range: {daily_health['date'].min()} to {daily_health['date'].max()}")
print(f"Selected features: {list(healthcare_features.keys())}")

# ==================== WEALTH INDEX ====================
print("\n" + "="*60)
print("EXTRACTING WEALTH INDEX FEATURES")
print("="*60)

print("\nLoading tm_relative_wealth_index.csv...")
wealth_df = pd.read_csv(os.path.join(project_root, 'app/data/tm_relative_wealth_index.csv'))

# Filter for Iloilo City barangays
print("Filtering for Iloilo City...")
iloilo_wealth = wealth_df[wealth_df['adm4_pcode'].isin(iloilo_brgys_set)].copy()
print(f"Iloilo City wealth records: {len(iloilo_wealth)}")

# Convert date
iloilo_wealth['date'] = pd.to_datetime(iloilo_wealth['date'])

# Select wealth index features
wealth_features = {
    'rwi_mean': 'mean',
    'rwi_median': 'mean',
    'rwi_std': 'mean',
}

print("\nAggregating wealth data by date...")
daily_wealth = iloilo_wealth.groupby('date').agg(wealth_features).reset_index()

print(f"\nAggregated wealth records: {len(daily_wealth)}")
print(f"Date range: {daily_wealth['date'].min()} to {daily_wealth['date'].max()}")
print(f"Selected features: {list(wealth_features.keys())}")

# ==================== MERGE FEATURES ====================
print("\n" + "="*60)
print("MERGING HEALTHCARE AND WEALTH DATA")
print("="*60)

# Merge healthcare and wealth
combined = daily_health.merge(daily_wealth, on='date', how='outer')
combined = combined.sort_values('date').reset_index(drop=True)

# Fill missing values
print("\nFilling missing values...")
feature_cols = list(healthcare_features.keys()) + list(wealth_features.keys())
for col in feature_cols:
    missing_count = combined[col].isna().sum()
    if missing_count > 0:
        print(f"  {col}: {missing_count} missing values - forward/backward filling")
        combined[col] = combined[col].ffill().bfill()

print(f"\nFinal combined records: {len(combined)}")
print(f"Date range: {combined['date'].min()} to {combined['date'].max()}")

# Save the processed data
output_file = os.path.join(project_root, 'app/data/iloilo_healthcare_wealth.csv')
combined.to_csv(output_file, index=False)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\nFeatures extracted: {len(feature_cols)}")
print(f"\nHealthcare Features (8):")
for feat in healthcare_features.keys():
    print(f"  - {feat}")
print(f"\nWealth Index Features (3):")
for feat in wealth_features.keys():
    print(f"  - {feat}")
print(f"\nTotal records: {len(combined)}")
print(f"Date coverage: {combined['date'].min()} to {combined['date'].max()}")
print(f"\n✓ Saved to: {output_file}")

print("\nSample data:")
print(combined.head(10))

print("\nStatistics:")
print(combined[feature_cols].describe())
