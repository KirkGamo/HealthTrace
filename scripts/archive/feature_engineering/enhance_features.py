"""
Enhanced CCHAIN Data Preparation - Adding Temperature and Additional Features
Extracts temperature, population, and nighttime lights data for Iloilo City
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Constants
ILOILO_CITY_CODE = 'PH063022000'  # adm3_pcode for Iloilo City
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(project_root, 'app', 'data')

def load_iloilo_barangays():
    """Get list of barangay codes for Iloilo City"""
    print("Loading Iloilo City barangay codes...")
    location_df = pd.read_csv(os.path.join(DATA_DIR, 'location.csv'))
    iloilo_brgys = location_df[
        location_df['adm3_pcode'] == ILOILO_CITY_CODE
    ]['adm4_pcode'].unique()
    print(f"  Found {len(iloilo_brgys)} barangays")
    return iloilo_brgys

def extract_temperature_data(iloilo_brgys):
    """
    Extract temperature data from large climate_atmosphere file
    Process in chunks to handle large file size
    """
    print("\nExtracting temperature data from climate_atmosphere.csv...")
    print("  (This may take a few minutes due to large file size...)")
    
    climate_file = os.path.join(DATA_DIR, 'climate_atmosphere.csv')
    
    # Process in chunks
    chunk_size = 100000
    temp_data = []
    
    try:
        for i, chunk in enumerate(pd.read_csv(climate_file, chunksize=chunk_size)):
            # Filter for Iloilo City barangays
            chunk_filtered = chunk[chunk['adm4_pcode'].isin(iloilo_brgys)].copy()
            
            if len(chunk_filtered) > 0:
                temp_data.append(chunk_filtered)
                print(f"    Processed chunk {i+1}: Found {len(chunk_filtered)} records")
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"    Progress: {(i+1) * chunk_size:,} rows processed...")
        
        if temp_data:
            df = pd.concat(temp_data, ignore_index=True)
            print(f"  ✓ Extracted {len(df)} temperature records")
            return df
        else:
            print("  ✗ No temperature data found for Iloilo City")
            return None
            
    except Exception as e:
        print(f"  ✗ Error reading temperature data: {e}")
        return None

def load_population_data(iloilo_brgys):
    """Load population data for Iloilo City"""
    print("\nLoading population data...")
    
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'worldpop_population.csv'))
        df = df[df['adm4_pcode'].isin(iloilo_brgys)].copy()
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"  ✓ Loaded {len(df)} population records")
        print(f"    Date range: {df['date'].min()} to {df['date'].max()}")
        
        return df
    except Exception as e:
        print(f"  ✗ Error loading population data: {e}")
        return None

def load_nighttime_lights(iloilo_brgys):
    """Load nighttime lights data for Iloilo City"""
    print("\nLoading nighttime lights data...")
    
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'nighttime_lights.csv'))
        df = df[df['adm4_pcode'].isin(iloilo_brgys)].copy()
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"  ✓ Loaded {len(df)} nighttime lights records")
        print(f"    Date range: {df['date'].min()} to {df['date'].max()}")
        
        return df
    except Exception as e:
        print(f"  ✗ Error loading nighttime lights data: {e}")
        return None

def aggregate_to_city_level(df, value_columns, date_col='date'):
    """Aggregate barangay-level data to city level"""
    agg_dict = {col: 'mean' for col in value_columns}
    result = df.groupby(date_col).agg(agg_dict).reset_index()
    return result

def process_temperature_data(temp_df):
    """Process and aggregate temperature data"""
    if temp_df is None or len(temp_df) == 0:
        return None
    
    print("\nProcessing temperature data...")
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    
    # Select temperature-related columns
    temp_cols = ['t2m_mean', 't2m_min', 't2m_max']  # 2-meter temperature
    available_cols = [col for col in temp_cols if col in temp_df.columns]
    
    if not available_cols:
        print("  ✗ No temperature columns found")
        return None
    
    print(f"  Available temperature columns: {available_cols}")
    
    # Aggregate to city level
    city_temp = aggregate_to_city_level(temp_df, available_cols)
    
    # Convert from Kelvin to Celsius if needed
    for col in available_cols:
        if city_temp[col].mean() > 100:  # Likely in Kelvin
            city_temp[col] = city_temp[col] - 273.15
    
    print(f"  ✓ Processed {len(city_temp)} daily temperature records")
    return city_temp

def merge_enhanced_features(base_df, temp_df, pop_df, lights_df):
    """Merge additional features with base disease data"""
    print("\nMerging enhanced features...")
    
    merged = base_df.copy()
    merge_count = 0
    
    # Merge temperature data (daily)
    if temp_df is not None and len(temp_df) > 0:
        merged = pd.merge(merged, temp_df, on='date', how='left')
        merge_count += 1
        print(f"  ✓ Merged temperature data")
    
    # Merge population data (need to handle different frequencies)
    if pop_df is not None and len(pop_df) > 0:
        pop_city = aggregate_to_city_level(
            pop_df, 
            ['pop_count_total', 'pop_density_mean']
        )
        # Forward fill population data
        merged['year'] = merged['date'].dt.year
        pop_city['year'] = pop_city['date'].dt.year
        pop_yearly = pop_city.groupby('year').first().reset_index()
        merged = pd.merge(merged, pop_yearly[['year', 'pop_count_total', 'pop_density_mean']], 
                         on='year', how='left')
        merged = merged.drop('year', axis=1)
        merge_count += 1
        print(f"  ✓ Merged population data")
    
    # Merge nighttime lights (annual)
    if lights_df is not None and len(lights_df) > 0:
        lights_city = aggregate_to_city_level(
            lights_df, 
            ['avg_rad_mean']
        )
        merged['year'] = merged['date'].dt.year
        lights_city['year'] = lights_city['date'].dt.year
        lights_yearly = lights_city.groupby('year').first().reset_index()
        merged = pd.merge(merged, lights_yearly[['year', 'avg_rad_mean']], 
                         on='year', how='left')
        merged = merged.drop('year', axis=1)
        merge_count += 1
        print(f"  ✓ Merged nighttime lights data")
    
    print(f"\n  Total features merged: {merge_count}")
    print(f"  Final shape: {merged.shape}")
    
    return merged

def update_disease_files_with_features():
    """Update existing disease files with enhanced features"""
    print("\n" + "="*60)
    print("ENHANCING DISEASE DATA WITH ADDITIONAL FEATURES")
    print("="*60)
    
    # Get Iloilo barangays
    iloilo_brgys = load_iloilo_barangays()
    
    # Load additional datasets
    temp_df = extract_temperature_data(iloilo_brgys)
    temp_processed = process_temperature_data(temp_df) if temp_df is not None else None
    
    pop_df = load_population_data(iloilo_brgys)
    lights_df = load_nighttime_lights(iloilo_brgys)
    
    # Process each disease file
    diseases = ['dengue', 'typhoid', 'cholera']
    
    for disease in diseases:
        print(f"\n{'='*60}")
        print(f"Processing {disease.upper()}")
        print(f"{'='*60}")
        
        # Load existing disease data
        disease_file = os.path.join(DATA_DIR, f'{disease}_historical_data.csv')
        
        if not os.path.exists(disease_file):
            print(f"  ✗ File not found: {disease_file}")
            continue
        
        df = pd.read_csv(disease_file, parse_dates=['date'])
        print(f"  Loaded {len(df)} existing records")
        print(f"  Existing columns: {df.columns.tolist()}")
        
        # Merge enhanced features
        enhanced_df = merge_enhanced_features(df, temp_processed, pop_df, lights_df)
        
        # Fill missing values
        print("\n  Handling missing values...")
        numeric_cols = enhanced_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != 'disease_cases':
                enhanced_df[col] = enhanced_df[col].ffill().bfill()
        
        # Save enhanced file
        output_file = os.path.join(DATA_DIR, f'{disease}_historical_data_enhanced.csv')
        enhanced_df.to_csv(output_file, index=False)
        
        print(f"\n  ✓ Saved enhanced data to: {disease}_historical_data_enhanced.csv")
        print(f"    Total columns: {len(enhanced_df.columns)}")
        print(f"    New columns added: {set(enhanced_df.columns) - set(df.columns)}")
        print(f"    Sample stats:")
        print(enhanced_df.describe())

def main():
    """Main execution"""
    print("Starting enhanced feature extraction...")
    print("This will add temperature, population, and nighttime lights data")
    print()
    
    update_disease_files_with_features()
    
    print("\n" + "="*60)
    print("✓ Enhanced feature extraction complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the enhanced files: *_historical_data_enhanced.csv")
    print("2. Update config.py to include new features")
    print("3. Retrain models: python train_model.py")

if __name__ == '__main__':
    main()
