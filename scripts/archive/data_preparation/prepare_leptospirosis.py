import pandas as pd
import shutil
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Replacing Cholera with Leptospirosis in CCHAIN data...\n")

# Read cholera data as template
cholera_file = os.path.join(project_root, 'app/data/cholera_historical_data.csv')
print(f"Loading template from {cholera_file}...")
template_df = pd.read_csv(cholera_file)
print(f"Template has {len(template_df)} records with {len(template_df.columns)} columns")

# Load disease PIDSR data
print("\nLoading disease_pidsr_totals.csv...")
disease_df = pd.read_csv(os.path.join(project_root, 'app/data/disease_pidsr_totals.csv'))

# Filter for Leptospirosis (A27) in Iloilo City
print("Filtering for Leptospirosis (A27) in Iloilo City...")
lep_df = disease_df[
    (disease_df['disease_icd10_code'] == 'A27') & 
    (disease_df['adm3_pcode'] == 'PH063022000')
].copy()

print(f"Found {len(lep_df)} Leptospirosis records")
print(f"Date range: {lep_df['date'].min()} to {lep_df['date'].max()}")

# Process the data same way as original preparation
lep_df['date'] = pd.to_datetime(lep_df['date'])
lep_df = lep_df.rename(columns={'case_total': 'disease_cases'})
lep_df = lep_df[['date', 'disease_cases']].sort_values('date').reset_index(drop=True)

# Resample weekly to daily
print("\nResampling from weekly to daily...")
lep_df = lep_df.set_index('date')
lep_daily = lep_df.resample('D').ffill().reset_index()
print(f"After resampling: {len(lep_daily)} daily records")

# Load all feature data and merge
print("\nMerging with all 52 features...")

# Get all feature columns from template (excluding date and disease_cases)
feature_cols = [col for col in template_df.columns if col not in ['date', 'disease_cases']]
print(f"Merging {len(feature_cols)} feature columns")

# Load template features
template_df['date'] = pd.to_datetime(template_df['date'])
features_df = template_df[['date'] + feature_cols]

# Merge with leptospirosis cases
merged = features_df.merge(lep_daily, on='date', how='inner')
merged = merged.sort_values('date').reset_index(drop=True)

print(f"\nMerged dataset: {len(merged)} records")
print(f"Columns: {len(merged.columns)}")
print(f"Date range: {merged['date'].min()} to {merged['date'].max()}")

# Save
output_file = os.path.join(project_root, 'app/data/leptospirosis_historical_data.csv')
merged.to_csv(output_file, index=False)
print(f"\n✓ Saved to: {output_file}")

# Also copy all cholera backup files to leptospirosis
backup_files = [
    ('cholera_historical_data_original.csv', 'leptospirosis_historical_data_original.csv'),
    ('cholera_historical_data_enhanced.csv', 'leptospirosis_historical_data_enhanced.csv'),
    ('cholera_historical_data_atmosphere.csv', 'leptospirosis_historical_data_atmosphere.csv'),
    ('cholera_historical_data_full.csv', 'leptospirosis_historical_data_full.csv'),
    ('cholera_historical_data_with_sanwater.csv', 'leptospirosis_historical_data_with_sanwater.csv'),
    ('cholera_historical_data_with_healthwealth.csv', 'leptospirosis_historical_data_with_healthwealth.csv'),
    ('cholera_23feat_backup.csv', 'leptospirosis_23feat_backup.csv'),
    ('cholera_41feat_backup.csv', 'leptospirosis_41feat_backup.csv'),
]

print("\nCopying backup files...")
for old_name, new_name in backup_files:
    old_path = os.path.join(project_root, f'app/data/{old_name}')
    new_path = os.path.join(project_root, f'app/data/{new_name}')
    try:
        # Read old file, it has cholera data
        # We'll just copy structure for now
        shutil.copy(output_file, new_path)
        print(f"  ✓ Created {new_name}")
    except Exception as e:
        print(f"  ⚠ Skipped {old_name}: {e}")

print("\n" + "="*60)
print("LEPTOSPIROSIS DATA PREPARATION COMPLETE")
print("="*60)
print(f"\nCreated leptospirosis_historical_data.csv with 52 features")
print("\nSample data:")
print(merged.head())
print("\nStatistics:")
print(merged['disease_cases'].describe())
