import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Extracting Air Quality and Vegetation features for Iloilo City...\n")

# Load location data to get Iloilo City barangays
print("Loading location data...")
location_df = pd.read_csv(os.path.join(project_root, 'app/data/location.csv'))
iloilo_brgys = location_df[location_df['adm3_pcode'] == 'PH063022000']['adm4_pcode'].tolist()
print(f"Found {len(iloilo_brgys)} barangays in Iloilo City")

# ==================== AIR QUALITY ====================
print("\n" + "="*60)
print("EXTRACTING AIR QUALITY FEATURES")
print("="*60)

print("\nLoading climate_air_quality.csv in chunks...")
chunk_size = 500000  # Larger chunks for faster processing
airqual_chunks = []

# Convert barangay list to set for faster lookup
iloilo_brgys_set = set(iloilo_brgys)

for i, chunk in enumerate(pd.read_csv(os.path.join(project_root, 'app/data/climate_air_quality.csv'), chunksize=chunk_size)):
    # Filter for Iloilo City barangays
    iloilo_chunk = chunk[chunk['adm4_pcode'].isin(iloilo_brgys_set)]
    if len(iloilo_chunk) > 0:
        airqual_chunks.append(iloilo_chunk)
    if (i + 1) % 2 == 0:
        print(f"  Processed {(i+1) * chunk_size:,} rows...")

print("\nCombining air quality chunks...")
iloilo_airqual = pd.concat(airqual_chunks, ignore_index=True)
print(f"Iloilo City air quality records: {len(iloilo_airqual)}")

# Convert date and aggregate by date
iloilo_airqual['date'] = pd.to_datetime(iloilo_airqual['date'])

print("Aggregating air quality data by date...")
daily_airqual = iloilo_airqual.groupby('date').agg({
    'no2': 'mean',      # Nitrogen dioxide (µg/m³)
    'co': 'mean',       # Carbon monoxide (mg/m³)
    'so2': 'mean',      # Sulfur dioxide (µg/m³)
    'o3': 'mean',       # Ozone (µg/m³)
    'pm10': 'mean',     # Particulate matter 10μm (µg/m³)
    'pm25': 'mean'      # Particulate matter 2.5μm (µg/m³)
}).reset_index()

print(f"\nAggregated air quality records: {len(daily_airqual)}")
print(f"Date range: {daily_airqual['date'].min()} to {daily_airqual['date'].max()}")

# ==================== VEGETATION (NDVI) ====================
print("\n" + "="*60)
print("EXTRACTING VEGETATION (NDVI) FEATURES")
print("="*60)

print("\nLoading climate_land.csv in chunks...")
land_chunks = []

for i, chunk in enumerate(pd.read_csv(os.path.join(project_root, 'app/data/climate_land.csv'), chunksize=chunk_size)):
    # Filter for Iloilo City barangays
    iloilo_chunk = chunk[chunk['adm4_pcode'].isin(iloilo_brgys_set)]
    if len(iloilo_chunk) > 0:
        land_chunks.append(iloilo_chunk)
    if (i + 1) % 2 == 0:
        print(f"  Processed {(i+1) * chunk_size:,} rows...")

print("\nCombining vegetation chunks...")
iloilo_land = pd.concat(land_chunks, ignore_index=True)
print(f"Iloilo City vegetation records: {len(iloilo_land)}")

# Convert date and aggregate by date
iloilo_land['date'] = pd.to_datetime(iloilo_land['date'])

print("Aggregating vegetation data by date...")
daily_land = iloilo_land.groupby('date').agg({
    'ndvi': 'mean'      # Normalized Difference Vegetation Index
}).reset_index()

print(f"\nAggregated vegetation records: {len(daily_land)}")
print(f"Date range: {daily_land['date'].min()} to {daily_land['date'].max()}")

# ==================== MERGE FEATURES ====================
print("\n" + "="*60)
print("MERGING AIR QUALITY AND VEGETATION DATA")
print("="*60)

# Merge air quality and vegetation
combined = daily_airqual.merge(daily_land, on='date', how='outer')
combined = combined.sort_values('date').reset_index(drop=True)

# Fill missing values (NDVI might have different date range)
print("\nFilling missing values...")
for col in ['no2', 'co', 'so2', 'o3', 'pm10', 'pm25', 'ndvi']:
    missing_count = combined[col].isna().sum()
    if missing_count > 0:
        print(f"  {col}: {missing_count} missing values - forward/backward filling")
        combined[col] = combined[col].ffill().bfill()

print(f"\nFinal combined records: {len(combined)}")
print(f"Date range: {combined['date'].min()} to {combined['date'].max()}")

# Save the processed data
output_file = os.path.join(project_root, 'app/data/iloilo_airqual_vegetation.csv')
combined.to_csv(output_file, index=False)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\nFeatures extracted: 7")
print(f"  Air Quality (6): no2, co, so2, o3, pm10, pm25")
print(f"  Vegetation (1): ndvi")
print(f"\nTotal records: {len(combined)}")
print(f"Date coverage: {combined['date'].min()} to {combined['date'].max()}")
print(f"\n✓ Saved to: {output_file}")

print("\nSample data:")
print(combined.head(10))

print("\nStatistics:")
print(combined[['no2', 'co', 'so2', 'o3', 'pm10', 'pm25', 'ndvi']].describe())
