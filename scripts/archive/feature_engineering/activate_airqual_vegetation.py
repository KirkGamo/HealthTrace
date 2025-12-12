import shutil
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Activating air quality and vegetation features...\n")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    # Backup current 16-feature files
    current_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    backup_file = os.path.join(project_root, f'app/data/{disease}_historical_data_16feat_backup.csv')
    
    if os.path.exists(current_file):
        shutil.copy(current_file, backup_file)
        print(f"✓ Backed up {disease}_historical_data.csv (16 features)")
    
    # Copy full feature files to main location
    full_file = os.path.join(project_root, f'app/data/{disease}_historical_data_full.csv')
    dest_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    
    shutil.copy(full_file, dest_file)
    print(f"✓ Activated {disease}_historical_data_full.csv -> {disease}_historical_data.csv")

print("\n" + "="*60)
print("Air quality and vegetation features activated!")
print("="*60)
print(f"Total features: 23 input features + 1 target = 24 columns")
print(f"\nNew environmental features added:")
print(f"  Air Quality (6):")
print(f"    - no2: Nitrogen dioxide (µg/m³)")
print(f"    - co: Carbon monoxide (mg/m³)")
print(f"    - so2: Sulfur dioxide (µg/m³)")
print(f"    - o3: Ozone (µg/m³)")
print(f"    - pm10: Particulate matter 10μm (µg/m³)")
print(f"    - pm25: Particulate matter 2.5μm (µg/m³)")
print(f"  Vegetation (1):")
print(f"    - ndvi: Normalized Difference Vegetation Index")
print(f"\nBackups saved as *_16feat_backup.csv")
