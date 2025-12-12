import shutil
import os

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Activating atmosphere-enhanced features...\n")

diseases = ['dengue', 'typhoid', 'cholera']

for disease in diseases:
    # Backup current enhanced files
    current_file = os.path.join(project_root, f'app/data/{disease}_historical_data_enhanced.csv')
    backup_file = os.path.join(project_root, f'app/data/{disease}_historical_data_enhanced_backup.csv')
    
    if os.path.exists(current_file):
        shutil.copy(current_file, backup_file)
        print(f"✓ Backed up {disease}_historical_data_enhanced.csv")
    
    # Copy atmosphere files to main location
    atmos_file = os.path.join(project_root, f'app/data/{disease}_historical_data_atmosphere.csv')
    dest_file = os.path.join(project_root, f'app/data/{disease}_historical_data.csv')
    
    shutil.copy(atmos_file, dest_file)
    print(f"✓ Activated {disease}_historical_data_atmosphere.csv -> {disease}_historical_data.csv")

print("\n" + "="*60)
print("Atmosphere features activated!")
print("="*60)
print(f"Total features: 16 input features + 1 target = 17 columns")
print(f"\nNew temperature features added:")
print(f"  - tmin: Minimum temperature (°C)")
print(f"  - tmax: Maximum temperature (°C)")
print(f"  - tave: Average temperature (°C)")
print(f"  - temp_range: Diurnal temperature range")
print(f"  - tave_7day: 7-day moving average temperature")
print(f"  - tave_30day: 30-day moving average temperature")
print(f"\nBackups saved as *_enhanced_backup.csv")
