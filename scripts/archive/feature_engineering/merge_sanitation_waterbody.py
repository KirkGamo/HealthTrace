import pandas as pd
import numpy as np
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Merging Sanitation/Water Body features with disease data...\n")

# Load the sanitation and water body data
print("Loading sanitation/water body features...")
san_water = pd.read_csv(os.path.join(project_root, 'app/data/iloilo_sanitation_waterbody.csv'))
san_water['date'] = pd.to_datetime(san_water['date'])
print(f"Sanitation/water body records: {len(san_water)}")
print(f"Date range: {san_water['date'].min()} to {san_water['date'].max()}")

# Get feature columns (all except date)
feature_cols = [col for col in san_water.columns if col != 'date']
print(f"\nFeatures to merge: {len(feature_cols)}")
for feat in feature_cols:
    print(f"  - {feat}")

# Process each disease
diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    print("\n" + "="*60)
    print(f"PROCESSING {disease.upper()}")
    print("="*60)
    
    # Load current disease data (23 features)
    input_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    print(f"\nLoading {input_file}...")
    disease_df = pd.read_csv(input_file)
    disease_df['date'] = pd.to_datetime(disease_df['date'])
    
    print(f"Current records: {len(disease_df)}")
    print(f"Current features: {len(disease_df.columns) - 1}")
    print(f"Date range: {disease_df['date'].min()} to {disease_df['date'].max()}")
    
    # Merge with sanitation/water body data
    print("\nMerging with sanitation/water body features...")
    merged = disease_df.merge(san_water, on='date', how='left')
    
    # Since sanitation data is yearly (only 9 records), we need to forward fill
    print("Forward filling yearly sanitation/water body values to daily...")
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
    output_file = os.path.join(project_root, f'app/data/{disease}_historical_data_with_sanwater.csv')
    merged.to_csv(output_file, index=False)
    
    print(f"\n✓ Saved: {output_file}")
    print(f"  Total records: {len(merged)}")
    print(f"  Total features: {len(merged.columns) - 1} (before: 23, added: {len(feature_cols)})")
    print(f"  Expected total: {23 + len(feature_cols)} = {23 + len(feature_cols)}")
    
    # Verify column count
    print("\nColumn verification:")
    print(f"  Columns in output: {len(merged.columns)}")
    print(f"  Expected (23 old + 18 new + 1 date): 42")
    
    # Show sample
    print("\nSample data (first 5 rows, last 10 columns):")
    print(merged[merged.columns[-10:]].head())

print("\n" + "="*60)
print("MERGE COMPLETE")
print("="*60)
print("\nAll disease datasets now have 41 features (23 environmental + 18 sanitation/water body)")
print("\nNext steps:")
print("1. Review the merged data")
print("2. Run activate_sanitation_waterbody.py to replace current data")
print("3. Update config.py with new feature list")
print("4. Retrain models with expanded feature set")
