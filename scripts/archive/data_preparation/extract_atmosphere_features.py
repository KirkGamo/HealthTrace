import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Loading location data to get Iloilo City barangays...")
location_df = pd.read_csv(os.path.join(project_root, 'app/data/location.csv'))
iloilo_brgys = location_df[location_df['adm3_pcode'] == 'PH063022000']['adm4_pcode'].tolist()
print(f"Found {len(iloilo_brgys)} barangays in Iloilo City")

print("\nLoading climate_atmosphere_downscaled.csv in chunks...")
chunk_size = 100000
iloilo_chunks = []

for i, chunk in enumerate(pd.read_csv(os.path.join(project_root, 'app/data/climate_atmosphere_downscaled.csv'), chunksize=chunk_size)):
    # Filter for Iloilo City barangays
    iloilo_chunk = chunk[chunk['adm4_pcode'].isin(iloilo_brgys)]
    if len(iloilo_chunk) > 0:
        iloilo_chunks.append(iloilo_chunk)
    if (i + 1) % 10 == 0:
        print(f"  Processed {(i+1) * chunk_size:,} rows...")

print("\nCombining filtered chunks...")
iloilo_atmos = pd.concat(iloilo_chunks, ignore_index=True)
print(f"Iloilo City records: {len(iloilo_atmos)}")

# Convert date to datetime
iloilo_atmos['date'] = pd.to_datetime(iloilo_atmos['date'])

# Aggregate by date (average across all barangays)
print("\nAggregating data by date...")
daily_climate = iloilo_atmos.groupby('date').agg({
    'tmin': 'mean',      # Minimum temperature (°C)
    'tmax': 'mean',      # Maximum temperature (°C)
    'tave': 'mean',      # Average temperature (°C)
    'pr': 'sum'          # Precipitation (mm) - sum across barangays
}).reset_index()

print(f"\nAggregated records: {len(daily_climate)}")
print(f"Date range: {daily_climate['date'].min()} to {daily_climate['date'].max()}")

# Calculate additional temperature features
print("\nCalculating additional temperature features...")
daily_climate['temp_range'] = daily_climate['tmax'] - daily_climate['tmin']  # Diurnal temperature range
daily_climate['tave_7day'] = daily_climate['tave'].rolling(window=7, min_periods=1).mean()  # 7-day moving average
daily_climate['tave_30day'] = daily_climate['tave'].rolling(window=30, min_periods=1).mean()  # 30-day moving average

print("\nFinal features:")
print(daily_climate.columns.tolist())
print("\nSample data:")
print(daily_climate.head(10))

print("\nStatistics:")
print(daily_climate.describe())

# Save the processed data
output_file = os.path.join(project_root, 'app/data/iloilo_climate_atmosphere.csv')
daily_climate.to_csv(output_file, index=False)
print(f"\n✓ Saved to: {output_file}")
