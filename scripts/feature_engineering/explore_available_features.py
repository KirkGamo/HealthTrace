import pandas as pd
import os

print("Exploring available CCHAIN datasets...\n")

data_dir = 'app/data'
cchain_files = {
    'climate_air_quality.csv': 'Air quality indices',
    'climate_land.csv': 'Land surface temperature, soil moisture, vegetation',
    'tm_relative_wealth_index.csv': 'Wealth indicators by location',
    'ookla_internet_speed.csv': 'Internet connectivity metrics',
    'esa_worldcover.csv': 'Land cover classification',
    'osm_poi_health.csv': 'Health facility locations',
    'osm_poi_sanitation.csv': 'Sanitation facilities',
    'osm_poi_water_body.csv': 'Water bodies',
    'project_noah_hazards.csv': 'Natural disaster/hazard data',
}

for filename, description in cchain_files.items():
    filepath = os.path.join(data_dir, filename)
    if os.path.exists(filepath):
        try:
            # Try to read first few rows
            df = pd.read_csv(filepath, nrows=5)
            file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            print(f"\n{'='*60}")
            print(f"File: {filename} ({file_size:.1f} MB)")
            print(f"Description: {description}")
            print(f"Columns ({len(df.columns)}): {df.columns.tolist()}")
            print(f"\nSample data:")
            print(df.head(2))
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"File: {filename}")
            print(f"Error reading: {e}")
    else:
        print(f"\n{filename}: Not found")

print("\n" + "="*60)
print("RECOMMENDATIONS:")
print("="*60)
print("\n1. HIGH PRIORITY - Direct disease correlation:")
print("   - climate_land.csv: Land surface temp, soil moisture, vegetation")
print("   - climate_air_quality.csv: Air quality affects respiratory diseases")
print("   - osm_poi_water_body.csv: Water bodies (mosquito breeding, waterborne diseases)")
print("   - osm_poi_sanitation.csv: Sanitation quality (cholera, typhoid)")

print("\n2. MEDIUM PRIORITY - Socioeconomic factors:")
print("   - tm_relative_wealth_index.csv: Wealth affects health access")
print("   - ookla_internet_speed.csv: Development indicator")
print("   - osm_poi_health.csv: Healthcare accessibility")

print("\n3. LOWER PRIORITY - Environmental context:")
print("   - esa_worldcover.csv: Land use patterns")
print("   - project_noah_hazards.csv: Disaster impacts on disease")
