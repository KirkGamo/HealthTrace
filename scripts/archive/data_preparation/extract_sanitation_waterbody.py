import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Extracting Sanitation and Water Body features for Iloilo City...\n")

# Load location data to get Iloilo City barangays
print("Loading location data...")
location_df = pd.read_csv(os.path.join(project_root, 'app/data/location.csv'))
iloilo_brgys = location_df[location_df['adm3_pcode'] == 'PH063022000']['adm4_pcode'].tolist()
iloilo_brgys_set = set(iloilo_brgys)
print(f"Found {len(iloilo_brgys)} barangays in Iloilo City")

# ==================== SANITATION ====================
print("\n" + "="*60)
print("EXTRACTING SANITATION FEATURES")
print("="*60)

print("\nLoading osm_poi_sanitation.csv...")
sanitation_df = pd.read_csv(os.path.join(project_root, 'app/data/osm_poi_sanitation.csv'))

# Filter for Iloilo City barangays
print("Filtering for Iloilo City...")
iloilo_sanitation = sanitation_df[sanitation_df['adm4_pcode'].isin(iloilo_brgys_set)].copy()
print(f"Iloilo City sanitation records: {len(iloilo_sanitation)}")

# Convert date
iloilo_sanitation['date'] = pd.to_datetime(iloilo_sanitation['date'])

# Select key sanitation features (avoid redundant ones)
# Focus on count and nearest distance for critical facilities
sanitation_features = {
    'drinking_water_count': 'mean',
    'drinking_water_nearest': 'mean',
    'water_well_count': 'mean',
    'water_well_nearest': 'mean',
    'toilet_count': 'mean',
    'toilet_nearest': 'mean',
    'waste_basket_count': 'mean',
    'waste_basket_nearest': 'mean',
    'wastewater_plant_count': 'mean',
    'wastewater_plant_nearest': 'mean',
}

print("\nAggregating sanitation data by date...")
daily_sanitation = iloilo_sanitation.groupby('date').agg(sanitation_features).reset_index()

print(f"\nAggregated sanitation records: {len(daily_sanitation)}")
print(f"Date range: {daily_sanitation['date'].min()} to {daily_sanitation['date'].max()}")
print(f"Selected features: {list(sanitation_features.keys())}")

# ==================== WATER BODIES ====================
print("\n" + "="*60)
print("EXTRACTING WATER BODY FEATURES")
print("="*60)

print("\nLoading osm_poi_water_body.csv...")
waterbody_df = pd.read_csv(os.path.join(project_root, 'app/data/osm_poi_water_body.csv'))

# Filter for Iloilo City barangays
print("Filtering for Iloilo City...")
iloilo_waterbody = waterbody_df[waterbody_df['adm4_pcode'].isin(iloilo_brgys_set)].copy()
print(f"Iloilo City water body records: {len(iloilo_waterbody)}")

# Convert date
iloilo_waterbody['date'] = pd.to_datetime(iloilo_waterbody['date'])

# Select key water body features (distance to various water sources)
waterbody_features = {
    'osm_wetland_nearest': 'mean',
    'osm_reservoir_nearest': 'mean',
    'osm_water_nearest': 'mean',
    'osm_riverbank_nearest': 'mean',
    'osm_river_nearest': 'mean',
    'osm_stream_nearest': 'mean',
    'osm_canal_nearest': 'mean',
    'osm_drain_nearest': 'mean',
}

print("\nAggregating water body data by date...")
daily_waterbody = iloilo_waterbody.groupby('date').agg(waterbody_features).reset_index()

print(f"\nAggregated water body records: {len(daily_waterbody)}")
print(f"Date range: {daily_waterbody['date'].min()} to {daily_waterbody['date'].max()}")
print(f"Selected features: {list(waterbody_features.keys())}")

# ==================== MERGE FEATURES ====================
print("\n" + "="*60)
print("MERGING SANITATION AND WATER BODY DATA")
print("="*60)

# Merge sanitation and water body
combined = daily_sanitation.merge(daily_waterbody, on='date', how='outer')
combined = combined.sort_values('date').reset_index(drop=True)

# Fill missing values
print("\nFilling missing values...")
feature_cols = list(sanitation_features.keys()) + list(waterbody_features.keys())
for col in feature_cols:
    missing_count = combined[col].isna().sum()
    if missing_count > 0:
        print(f"  {col}: {missing_count} missing values - forward/backward filling")
        combined[col] = combined[col].ffill().bfill()

print(f"\nFinal combined records: {len(combined)}")
print(f"Date range: {combined['date'].min()} to {combined['date'].max()}")

# Save the processed data
output_file = os.path.join(project_root, 'app/data/iloilo_sanitation_waterbody.csv')
combined.to_csv(output_file, index=False)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\nFeatures extracted: {len(feature_cols)}")
print(f"\nSanitation Features (10):")
for feat in sanitation_features.keys():
    print(f"  - {feat}")
print(f"\nWater Body Features (8):")
for feat in waterbody_features.keys():
    print(f"  - {feat}")
print(f"\nTotal records: {len(combined)}")
print(f"Date coverage: {combined['date'].min()} to {combined['date'].max()}")
print(f"\n✓ Saved to: {output_file}")

print("\nSample data:")
print(combined.head(10))

print("\nStatistics:")
print(combined[feature_cols].describe())
