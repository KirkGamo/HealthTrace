# CCHAIN Data Integration for HealthTrace

## Overview
This document describes the integration of Project CCHAIN (Climate Change and Health Impact Network) data from Kaggle into the HealthTrace disease forecasting system.

## Changes Made

### 1. Data Source
- **Original**: Synthetic data generated programmatically
- **Updated**: Real-world data from Project CCHAIN on Kaggle
- **Location**: Iloilo City, Philippines (adm3_pcode: PH063022000)
- **Time Period**: 2008-2022 (weekly disease data)

### 2. Diseases Tracked
**Previous**: Dengue, Influenza, Typhoid, Malaria
**Updated**: 
- Dengue Fever (ICD-10: A90-A91)
- Typhoid Fever (ICD-10: A01)
- Cholera (ICD-10: A00)

### 3. Climate Features
**Previous Features**:
- Temperature (°C)
- Humidity (%)
- Rainfall (mm)

**Updated Features (CCHAIN)**:
- `precipitation`: Normalized precipitation
- `spi3`: 3-month Standardized Precipitation Index
- `spi6`: 6-month Standardized Precipitation Index
- `precip_anomaly`: Precipitation anomaly (PNP)
- `precipitation_7day`: 7-day rolling average
- `precipitation_30day`: 30-day rolling average

### 4. Data Processing Pipeline

#### Step 1: Data Preparation
Run `prepare_cchain_data.py` to process raw CCHAIN data:
```powershell
python prepare_cchain_data.py
```

This script:
- Filters disease data for Iloilo City from `disease_pidsr_totals.csv`
- Aggregates climate data from barangay level to city level
- Merges weekly disease cases with monthly climate indices
- Resamples weekly data to daily using forward-fill
- Adds derived features (rolling averages, lags)
- Generates separate CSV files for each disease

#### Step 2: Model Training
Train LSTM models with the processed data:
```powershell
python train_model.py
```

This will:
- Load processed CCHAIN data for each disease
- Train LSTM models with variable feature counts
- Save models to `app/models/`

#### Step 3: Run Application
Start the Flask web application:
```powershell
python app.py
```

## File Changes

### Modified Files

1. **`prepare_cchain_data.py`** (NEW)
   - Main data processing script
   - Filters and transforms CCHAIN data for Iloilo City
   - Generates disease-specific CSV files

2. **`app/data_utils.py`**
   - Updated `prepare_features()` to handle both synthetic and CCHAIN data formats
   - Added automatic feature detection
   - Enhanced missing value handling

3. **`config.py`**
   - Updated `DISEASES` list: ['Dengue', 'Typhoid', 'Cholera']
   - Updated `CLIMATE_FEATURES` to match CCHAIN format

4. **`train_model.py`**
   - Removed synthetic data generation
   - Added check to ensure CCHAIN data is prepared first
   - Updated to use Config.DISEASES

5. **`app.py`**
   - Dynamic feature count detection for model initialization
   - Updated climate API endpoint to handle CCHAIN features
   - Backward compatible with legacy data format

### Data Files Structure

```
app/data/
├── disease.csv                          # Disease code mappings
├── location.csv                         # Location codes and names
├── disease_pidsr_totals.csv            # Raw weekly disease cases
├── climate_indices.csv                  # Raw monthly climate data
├── dengue_historical_data.csv          # Processed (generated)
├── typhoid_historical_data.csv         # Processed (generated)
└── cholera_historical_data.csv         # Processed (generated)
```

### Processed Data Format

Each disease CSV has the following columns:
```
date,precipitation,spi3,spi6,precip_anomaly,precipitation_7day,precipitation_30day,disease_cases
```

## Data Statistics (Example)

**Iloilo City - Dengue Fever**
- Records: ~5,200+ daily records
- Date Range: 2008-01-07 to 2022-12-31
- Features: 7 climate features + disease cases

## Usage Instructions

### First Time Setup
1. Download Project CCHAIN dataset from Kaggle
2. Extract to `app/data/` directory
3. Run data preparation: `python prepare_cchain_data.py`
4. Train models: `python train_model.py`
5. Start application: `python app.py`

### Subsequent Runs
If data is already processed:
```powershell
python app.py
```

## API Endpoints

### Get Forecast
```
GET /api/forecast/<disease>
```
Returns 14-day forecast with historical context.

**Diseases**: `Dengue`, `Typhoid`, `Cholera`

### Get Current Status
```
GET /api/current_status
```
Returns current status for all diseases.

### Get Climate Data
```
GET /api/climate_data/<disease>
```
Returns climate features for the last 30 days.

Response includes CCHAIN features:
- `precipitation`
- `spi3`, `spi6`
- `precip_anomaly`
- `precipitation_7day`, `precipitation_30day`

## Model Architecture

The LSTM models automatically adapt to the feature count:
- **Input Shape**: (sequence_length=30, n_features=7)
- **LSTM Layer 1**: 64 units
- **LSTM Layer 2**: 32 units
- **Output**: Single value (predicted cases)

## Key Improvements

1. **Real-World Data**: Actual disease surveillance data from DOH Philippines
2. **Location-Specific**: Focused on Iloilo City for accurate local predictions
3. **Rich Climate Features**: Multiple precipitation indices and anomaly detection
4. **Temporal Resolution**: Daily predictions from weekly surveillance data
5. **Flexible Architecture**: Handles variable feature counts automatically

## Troubleshooting

**Error: Data file not found**
- Solution: Run `python prepare_cchain_data.py` first

**Error: CCHAIN files missing**
- Solution: Download Project CCHAIN dataset from Kaggle
- Place in `app/data/` directory

**Low model accuracy**
- Consider: Adjusting sequence_length in config.py
- Consider: Increasing training epochs in train_model.py
- Consider: Adding more features from CCHAIN dataset

## References

- **Project CCHAIN**: Climate Change and Health Impact Network
- **Data Source**: Kaggle - Project CCHAIN Dataset
- **Location**: Iloilo City, Region VI, Philippines
- **Disease Source**: PIDSR-DOH (Philippine Integrated Disease Surveillance and Response)
- **Climate Source**: ERA5 Climate Reanalysis Data

## Future Enhancements

- [ ] Integrate additional CCHAIN features (temperature, land data)
- [ ] Add more Philippine cities
- [ ] Include air quality indices
- [ ] Incorporate population density data
- [ ] Add socioeconomic indicators
