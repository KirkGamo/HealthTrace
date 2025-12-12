"""
Script to activate enhanced features in HealthTrace
Replaces standard files with enhanced versions and updates configuration
"""

import os
import shutil
from pathlib import Path

# Set up project root path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = Path(project_root) / 'app' / 'data'
DISEASES = ['dengue', 'typhoid', 'cholera']

def backup_original_files():
    """Backup original disease files"""
    print("Backing up original files...")
    for disease in DISEASES:
        original = DATA_DIR / f'{disease}_historical_data.csv'
        backup = DATA_DIR / f'{disease}_historical_data_original.csv'
        
        if original.exists() and not backup.exists():
            shutil.copy2(original, backup)
            print(f"  ✓ Backed up {disease}_historical_data.csv")

def activate_enhanced_files():
    """Replace original files with enhanced versions"""
    print("\nActivating enhanced files...")
    for disease in DISEASES:
        enhanced = DATA_DIR / f'{disease}_historical_data_enhanced.csv'
        target = DATA_DIR / f'{disease}_historical_data.csv'
        
        if enhanced.exists():
            shutil.copy2(enhanced, target)
            print(f"  ✓ Activated enhanced data for {disease}")
        else:
            print(f"  ✗ Enhanced file not found for {disease}")

def update_config():
    """Update config.py with new features"""
    print("\nUpdating config.py...")
    
    config_path = Path('config.py')
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    # New feature list
    new_features = """    # Features for prediction (CCHAIN enhanced data format)
    CLIMATE_FEATURES = ['precipitation', 'spi3', 'spi6', 'precip_anomaly', 
                       'precipitation_7day', 'precipitation_30day',
                       'pop_count_total', 'pop_density_mean', 'avg_rad_mean']
    HEALTH_FEATURES = ['disease_cases']"""
    
    # Find and replace the old features section
    old_pattern_start = "    # Features for prediction (CCHAIN data format)"
    old_pattern_end = "    HEALTH_FEATURES = ['disease_cases']"
    
    start_idx = content.find(old_pattern_start)
    if start_idx != -1:
        end_idx = content.find(old_pattern_end, start_idx) + len(old_pattern_end)
        new_content = content[:start_idx] + new_features + content[end_idx:]
        
        with open(config_path, 'w') as f:
            f.write(new_content)
        
        print("  ✓ Updated CLIMATE_FEATURES in config.py")
        print("    Added: pop_count_total, pop_density_mean, avg_rad_mean")
    else:
        print("  ⚠ Could not auto-update config.py - please update manually")

def show_feature_summary():
    """Display summary of enhanced features"""
    print("\n" + "="*60)
    print("ENHANCED FEATURES SUMMARY")
    print("="*60)
    
    print("\nOriginal Features (7):")
    print("  • precipitation - Normalized precipitation")
    print("  • spi3 - 3-month Standardized Precipitation Index")
    print("  • spi6 - 6-month Standardized Precipitation Index")
    print("  • precip_anomaly - Precipitation anomaly")
    print("  • precipitation_7day - 7-day rolling average")
    print("  • precipitation_30day - 30-day rolling average")
    print("  • disease_cases - Target variable")
    
    print("\nNew Features Added (3):")
    print("  • pop_count_total - Total population count")
    print("  • pop_density_mean - Mean population density (people/km²)")
    print("  • avg_rad_mean - Average nighttime radiance (economic activity proxy)")
    
    print("\n📊 Total Features: 10 (9 input + 1 target)")
    
    print("\n" + "="*60)

def main():
    print("="*60)
    print("ACTIVATING ENHANCED FEATURES FOR HEALTHTRACE")
    print("="*60)
    print()
    
    # Backup originals
    backup_original_files()
    
    # Activate enhanced versions
    activate_enhanced_files()
    
    # Update config
    update_config()
    
    # Show summary
    show_feature_summary()
    
    print("\n✓ Enhanced features activated successfully!")
    print("\nNext steps:")
    print("  1. Retrain models: python train_model.py")
    print("  2. Restart Flask app: python app.py")
    print("\nNote: Models will now use 9 input features instead of 7")

if __name__ == '__main__':
    main()
