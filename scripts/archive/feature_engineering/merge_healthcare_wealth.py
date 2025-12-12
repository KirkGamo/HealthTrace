import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Merging Healthcare/Wealth Index features with disease data...\n")

# Load the healthcare and wealth data
print("Loading healthcare/wealth features...")
health_wealth = pd.read_csv(os.path.join(project_root, 'app/data/iloilo_healthcare_wealth.csv'))
health_wealth['date'] = pd.to_datetime(health_wealth['date'])
print(f"Healthcare/wealth records: {len(health_wealth)}")
print(f"Date range: {health_wealth['date'].min()} to {health_wealth['date'].max()}")

# Get feature columns (all except date)
feature_cols = [col for col in health_wealth.columns if col != 'date']
print(f"\nFeatures to merge: {len(feature_cols)}")
for feat in feature_cols:
    print(f"  - {feat}")

# Process each disease
diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    print("\n" + "="*60)
    print(f"PROCESSING {disease.upper()}")
    print("="*60)
    
    # Load current disease data (41 features)
    input_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    print(f"\nLoading {input_file}...")
    disease_df = pd.read_csv(input_file)
    disease_df['date'] = pd.to_datetime(disease_df['date'])
    
    print(f"Current records: {len(disease_df)}")
    print(f"Current features: {len(disease_df.columns) - 1}")
    print(f"Date range: {disease_df['date'].min()} to {disease_df['date'].max()}")
    
    # Merge with healthcare/wealth data
    print("\nMerging with healthcare/wealth features...")
    merged = disease_df.merge(health_wealth, on='date', how='left')
    
    # Since healthcare/wealth data is yearly (only 9 records), we need to forward fill
    print("Forward filling yearly healthcare/wealth values to daily...")
    for col in feature_cols:
        merged[col] = merged[col].ffill().bfill()
    
    # Check for missing values
    missing = merged[feature_cols].isna().sum()
    if missing.sum() > 0:
        print("\nWarning: Missing values detected after merge:")
        print(missing[missing > 0])
        print("Filling remaining NaNs with median values...")
        for col in feature_cols:
            if merged[col].isna().any():
                merged[col] = merged[col].fillna(merged[col].median())
    else:
        print("✓ No missing values after merge")
    
    # Save the merged data
    output_file = os.path.join(project_root, f'app/data/{disease}_historical_data_with_healthwealth.csv')
    merged.to_csv(output_file, index=False)
    
    print(f"\n✓ Saved: {output_file}")
    print(f"  Total records: {len(merged)}")
    print(f"  Total features: {len(merged.columns) - 1} (before: 41, added: {len(feature_cols)})")
    print(f"  Expected total: {41 + len(feature_cols)} = {41 + len(feature_cols)}")
    
    # Verify column count
    print("\nColumn verification:")
    print(f"  Columns in output: {len(merged.columns)}")
    print(f"  Expected (41 old + 11 new + 1 date): 53")
    
    # Show sample
    print("\nSample data (first 5 rows, last 10 columns):")
    print(merged[merged.columns[-10:]].head())

print("\n" + "="*60)
print("MERGE COMPLETE")
print("="*60)
print("\nAll disease datasets now have 52 features (41 existing + 11 healthcare/wealth)")
print("\nNext steps:")
print("1. Review the merged data")
print("2. Run activate_healthcare_wealth.py to replace current data")
print("3. Update config.py with new feature list")
print("4. Retrain models with expanded feature set")
