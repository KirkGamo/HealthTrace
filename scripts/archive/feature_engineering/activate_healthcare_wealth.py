import shutil
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Activating Healthcare/Wealth enhanced data...\n")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    print(f"Processing {disease}...")
    
    # Paths
    current_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    backup_file = os.path.join(project_root, f'app/data/{disease}_41feat_backup.csv')
    new_file = os.path.join(project_root, f'app/data/{disease}_historical_data_with_healthwealth.csv')
    
    # Backup current 41-feature data
    if os.path.exists(current_file):
        print(f"  Backing up current data to {backup_file}")
        shutil.copy(current_file, backup_file)
    
    # Replace with 52-feature data
    print(f"  Activating 52-feature data from {new_file}")
    shutil.copy(new_file, current_file)
    
    print(f"  ✓ {disease} data updated\n")

print("="*60)
print("ACTIVATION COMPLETE")
print("="*60)
print("\n✓ All disease datasets now use 52-feature data (41 + 11 healthcare/wealth)")
print("✓ Previous 41-feature data backed up as *_41feat_backup.csv")
print("\nNext steps:")
print("1. Update config.py CLIMATE_FEATURES list")
print("2. Update app/data_utils.py feature extraction")
print("3. Retrain models with 52 features")
