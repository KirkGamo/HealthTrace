"""
Prepare Project CCHAIN dataset for HealthTrace application
Filters data for Iloilo City and integrates disease cases with climate features
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Constants
ILOILO_CITY_CODE = 'PH063022000'  # adm3_pcode for Iloilo City
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(project_root, 'app', 'data')

# Disease mappings from CCHAIN to HealthTrace
DISEASE_MAPPING = {
    'A90-A91': 'dengue',      # Dengue Fever
    'A01': 'typhoid',          # Typhoid Fever
    'A00': 'cholera'           # Cholera
}

def load_disease_data():
    """Load PIDSR disease data for Iloilo City"""
    print("Loading disease data...")
    df = pd.read_csv(os.path.join(DATA_DIR, 'disease_pidsr_totals.csv'))
    
    # Filter for Iloilo City
    df = df[df['adm3_pcode'] == ILOILO_CITY_CODE].copy()
    
    # Filter for diseases of interest
    df = df[df['disease_icd10_code'].isin(DISEASE_MAPPING.keys())].copy()
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Map disease codes to simplified names
    df['disease'] = df['disease_icd10_code'].map(DISEASE_MAPPING)
    
    print(f"  Loaded {len(df)} disease records for Iloilo City")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Diseases: {df['disease'].unique()}")
    
    return df

def load_climate_data():
    """Load climate indices data for Iloilo City barangays"""
    print("Loading climate data...")
    df = pd.read_csv(os.path.join(DATA_DIR, 'climate_indices.csv'))
    
    # Get Iloilo City barangay codes from location file
    location_df = pd.read_csv(os.path.join(DATA_DIR, 'location.csv'))
    iloilo_brgys = location_df[
        location_df['adm3_pcode'] == ILOILO_CITY_CODE
    ]['adm4_pcode'].unique()
    
    # Filter for Iloilo City barangays
    df = df[df['adm4_pcode'].isin(iloilo_brgys)].copy()
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Aggregate to city level (average across barangays)
    climate_agg = df.groupby('date').agg({
        'pr_norm': 'mean',      # Normalized precipitation
        'spi3': 'mean',          # 3-month Standardized Precipitation Index
        'spi6': 'mean',          # 6-month Standardized Precipitation Index
        'pnp': 'mean'            # Precipitation anomaly
    }).reset_index()
    
    print(f"  Loaded {len(climate_agg)} monthly climate records for Iloilo City")
    print(f"  Date range: {climate_agg['date'].min()} to {climate_agg['date'].max()}")
    
    return climate_agg

def resample_weekly_to_daily(disease_df):
    """Convert weekly disease data to daily by forward filling"""
    print("Converting weekly to daily data...")
    
    # Create a complete date range
    date_range = pd.date_range(
        start=disease_df['date'].min(),
        end=disease_df['date'].max(),
        freq='D'
    )
    
    daily_data = []
    
    for disease in disease_df['disease'].unique():
        disease_subset = disease_df[disease_df['disease'] == disease].copy()
        disease_subset = disease_subset.sort_values('date')
        
        # Create daily dataframe
        daily_df = pd.DataFrame({'date': date_range})
        
        # Merge with disease data
        daily_df = pd.merge(daily_df, disease_subset[['date', 'case_total']], 
                           on='date', how='left')
        
        # Forward fill weekly values to daily
        daily_df['case_total'] = daily_df['case_total'].ffill()
        daily_df['case_total'] = daily_df['case_total'].fillna(0)  # Fill initial NaNs
        
        daily_df['disease'] = disease
        daily_data.append(daily_df)
    
    result = pd.concat(daily_data, ignore_index=True)
    print(f"  Created {len(result)} daily records")
    
    return result

def merge_climate_to_daily(daily_disease_df, climate_df):
    """Merge monthly climate data to daily disease data"""
    print("Merging climate data with disease data...")
    
    # Add year-month column for merging
    daily_disease_df['year_month'] = daily_disease_df['date'].dt.to_period('M')
    climate_df['year_month'] = climate_df['date'].dt.to_period('M')
    
    # Merge on year-month
    merged = pd.merge(
        daily_disease_df,
        climate_df[['year_month', 'pr_norm', 'spi3', 'spi6', 'pnp']],
        on='year_month',
        how='left'
    )
    
    # Drop year_month column
    merged = merged.drop('year_month', axis=1)
    
    # Handle infinite values in climate data
    merged = merged.replace([np.inf, -np.inf], np.nan)
    
    # Forward fill climate data
    for col in ['pr_norm', 'spi3', 'spi6', 'pnp']:
        merged[col] = merged.groupby('disease')[col].ffill()
        merged[col] = merged.groupby('disease')[col].bfill()
    
    print(f"  Merged data shape: {merged.shape}")
    
    return merged

def add_derived_features(df):
    """Add derived climate features"""
    print("Adding derived features...")
    
    # Rolling averages for precipitation
    df = df.sort_values(['disease', 'date'])
    
    for disease in df['disease'].unique():
        mask = df['disease'] == disease
        
        # 7-day rolling average of precipitation
        df.loc[mask, 'pr_7day_avg'] = df.loc[mask, 'pr_norm'].rolling(
            window=7, min_periods=1
        ).mean()
        
        # 30-day rolling average of precipitation
        df.loc[mask, 'pr_30day_avg'] = df.loc[mask, 'pr_norm'].rolling(
            window=30, min_periods=1
        ).mean()
        
        # Lagged disease cases (7 days prior)
        df.loc[mask, 'cases_lag7'] = df.loc[mask, 'case_total'].shift(7)
        
        # Lagged disease cases (14 days prior)
        df.loc[mask, 'cases_lag14'] = df.loc[mask, 'case_total'].shift(14)
    
    # Fill NaN values in lagged features
    df['cases_lag7'] = df['cases_lag7'].fillna(0)
    df['cases_lag14'] = df['cases_lag14'].fillna(0)
    
    print("  Added rolling averages and lagged features")
    
    return df

def save_disease_files(merged_df):
    """Save individual disease CSV files"""
    print("Saving disease-specific files...")
    
    for disease in merged_df['disease'].unique():
        disease_df = merged_df[merged_df['disease'] == disease].copy()
        disease_df = disease_df.sort_values('date')
        
        # Select final features
        output_df = disease_df[[
            'date', 'pr_norm', 'spi3', 'spi6', 'pnp', 
            'pr_7day_avg', 'pr_30day_avg', 'case_total'
        ]].copy()
        
        # Rename columns to match original format
        output_df.columns = [
            'date', 'precipitation', 'spi3', 'spi6', 'precip_anomaly',
            'precipitation_7day', 'precipitation_30day', 'disease_cases'
        ]
        
        # Save to file
        output_file = os.path.join(DATA_DIR, f'{disease}_historical_data.csv')
        output_df.to_csv(output_file, index=False)
        
        print(f"  Saved {disease}: {len(output_df)} records to {output_file}")
        print(f"    Date range: {output_df['date'].min()} to {output_df['date'].max()}")
        print(f"    Total cases: {output_df['disease_cases'].sum()}")

def generate_summary_report(merged_df):
    """Generate a summary report of the processed data"""
    print("\n" + "="*60)
    print("DATA PROCESSING SUMMARY")
    print("="*60)
    
    print(f"\nLocation: Iloilo City (Code: {ILOILO_CITY_CODE})")
    print(f"Overall date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
    print(f"Total records: {len(merged_df)}")
    
    print("\nDisease Statistics:")
    for disease in sorted(merged_df['disease'].unique()):
        disease_df = merged_df[merged_df['disease'] == disease]
        print(f"\n  {disease.upper()}:")
        print(f"    Total cases: {disease_df['case_total'].sum():.0f}")
        print(f"    Average weekly cases: {disease_df['case_total'].mean():.2f}")
        print(f"    Max weekly cases: {disease_df['case_total'].max():.0f}")
        print(f"    Records: {len(disease_df)}")
    
    print("\nClimate Features:")
    print(f"  Precipitation (pr_norm): {merged_df['pr_norm'].mean():.2f} ± {merged_df['pr_norm'].std():.2f}")
    print(f"  SPI-3: {merged_df['spi3'].mean():.2f} ± {merged_df['spi3'].std():.2f}")
    print(f"  SPI-6: {merged_df['spi6'].mean():.2f} ± {merged_df['spi6'].std():.2f}")
    print(f"  Precip Anomaly (pnp): {merged_df['pnp'].mean():.2f} ± {merged_df['pnp'].std():.2f}")
    
    print("\n" + "="*60)

def main():
    """Main processing pipeline"""
    print("="*60)
    print("CCHAIN DATA PREPARATION FOR HEALTHTRACE")
    print("="*60)
    print()
    
    # Load raw data
    disease_df = load_disease_data()
    climate_df = load_climate_data()
    
    # Process data
    daily_disease_df = resample_weekly_to_daily(disease_df)
    merged_df = merge_climate_to_daily(daily_disease_df, climate_df)
    merged_df = add_derived_features(merged_df)
    
    # Save processed files
    save_disease_files(merged_df)
    
    # Generate summary
    generate_summary_report(merged_df)
    
    print("\n✓ Data preparation complete!")
    print("  You can now train models using: python train_model.py")

if __name__ == '__main__':
    main()
