# HealthTrace - Disease Outbreak Forecasting System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange)

A Python-based web application to forecast disease outbreaks in the Philippines using deep learning models (LSTM/GRU) with TensorFlow. The application processes historical climate and health data to predict future disease incidence and provides an interactive dashboard for public health officials.

**Course:** Artificial Neural Network  
**Authors:** Ethan Jed Carbonell and Kirk Henrich Gamo

## Features

- 🤖 **Dual Model Architecture**: LSTM & GRU neural networks for time-series forecasting
- 📊 **Interactive Dashboard**: Real-time visualization with correlation-based feature impact analysis
- 🌡️ **Comprehensive Climate Integration**: 52+ features including temperature, humidity, rainfall, air quality, vegetation indices
- ⚠️ **Early Warning System**: Alert levels based on predicted outbreak severity
- 🏥 **Multi-Disease Support**: Tracks Dengue, Typhoid, and Leptospirosis
- 📈 **14-Day Forecasts**: Predicts disease cases two weeks in advance
- 🎨 **Modern UI/UX**: Gradient backgrounds, smooth animations, toast notifications
- ⚡ **Optimized Models**: 25.2% accuracy improvement through hyperparameter tuning
- 📊 **Feature Impact Analysis**: Interactive tabbed navigation with 9 feature categories
- 🔄 **Model Comparison**: Switch between LSTM and GRU architectures

## Project Structure

```
HealthTrace/
├── app/                        # Main application package
│   ├── data/                   # Historical climate and health data (52+ features)
│   ├── models/                 # Trained LSTM/GRU models (.h5 files)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Dashboard styling with animations
│   │   └── js/
│   │       └── dashboard.js   # Frontend JavaScript with interactive features
│   ├── templates/
│   │   └── index.html         # Main dashboard template
│   ├── data_utils.py          # Data processing and feature engineering utilities
│   ├── model.py               # LSTM/GRU model implementation
│   └── __init__.py            # Package initialization
│
├── scripts/                    # Utility scripts organized by purpose
│   ├── archive/               # Archived one-time scripts (reference only)
│   │   ├── data_preparation/  # Historical data extraction scripts
│   │   │   ├── prepare_cchain_data.py
│   │   │   ├── prepare_leptospirosis.py
│   │   │   ├── extract_airqual_vegetation.py
│   │   │   ├── extract_atmosphere_features.py
│   │   │   ├── extract_healthcare_wealth.py
│   │   │   └── extract_sanitation_waterbody.py
│   │   ├── feature_engineering/  # Feature activation and merging
│   │   │   ├── activate_*.py     # Feature set switchers
│   │   │   ├── merge_*.py        # Feature dataset mergers
│   │   │   ├── enhance_features.py
│   │   │   ├── explore_atmosphere_data.py
│   │   │   └── explore_available_features.py
│   │   ├── verification/      # One-time model checks
│   │   │   ├── check_leptospirosis.py
│   │   │   ├── check_model_shape.py
│   │   │   ├── verify_atmosphere_models.py
│   │   │   └── verify_sanwater_models.py
│   │   └── utilities/         # Temporary fix scripts
│   │       └── quick_fix_revert.py
│   │
│   ├── testing/               # Active test scripts
│   │   ├── test_app.py
│   │   ├── test_atmosphere_features.py
│   │   ├── test_features.py
│   │   ├── test_fixes.py
│   │   └── test_full_features.py
│   │
│   ├── verification/          # Active model verification
│   │   ├── compare_models.py      # LSTM vs GRU comparison
│   │   ├── verify_full_models.py  # 52-feature model validation
│   │   └── verify_healthwealth_models.py
│   │
│   └── utilities/             # Active optimization tools
│       └── hyperparameter_tuning.py  # Config optimization framework
│
├── docs/                       # Documentation and project reports
│   ├── BEST_CONFIGURATION.md  # Hyperparameter tuning results
│   ├── CCHAIN_INTEGRATION.md  # Climate data integration guide
│   ├── ENHANCED_FEATURES_GUIDE.md
│   ├── HYPERPARAMETER_TUNING.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── INTEGRATION_SUMMARY.md
│   ├── PULL_REQUEST.md        # Feature impact & UI/UX PR
│   ├── PULL_REQUEST_GRU.md    # GRU model implementation PR
│   └── PULL_REQUEST_HYPERPARAMETER.md  # Optimization PR
│
├── hyperparameter_results/    # Tuning experiment results
│   ├── *_tuning_*.json        # Detailed training history
│   └── *_summary_*.csv        # Comparison tables
│
├── app.py                     # Flask backend application
├── config.py                  # Configuration settings
├── train_model.py             # Model training script (optimized)
├── run_app.py                 # Application runner
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/KirkGamo/HealthTrace.git
   cd HealthTrace
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample data and train models**
   ```bash
   python train_model.py
   ```
   
   This will:
   - Generate synthetic historical data for 4 diseases (2 years of data each)
   - Train LSTM models for each disease
   - Save trained models to `app/models/`
   
   Training may take 10-20 minutes depending on your hardware.

5. **Run the application**
   ```bash
   python app.py
   ```
   
   The application will be available at: `http://localhost:5000`

## Usage

### Web Dashboard

1. **View Current Status**: The dashboard displays current disease cases and trends
2. **Select a Disease**: Click on any disease button (Dengue, Typhoid, Leptospirosis)
3. **View Forecasts**: See 14-day predictions with historical context
4. **Monitor Alerts**: Check alert levels (LOW, MEDIUM, HIGH) based on predictions
5. **Analyze Climate**: View climate factors affecting disease patterns
6. **Explore Feature Impact**: Interactive correlation-based impact analysis with 52+ features

### Scripts Organization

The repository includes various utility scripts organized by purpose:

**Data Preparation** (`scripts/data_preparation/`):
- Extract and prepare climate data from various sources
- Process disease case data
- Integrate CCHAIN climate datasets

**Feature Engineering** (`scripts/feature_engineering/`):
- Activate and merge additional features (air quality, vegetation, healthcare, sanitation)
- Explore available features and their distributions
- Enhance feature sets for improved model performance

**Testing** (`scripts/testing/`):
- Unit tests for application functionality
- Feature validation tests
- Integration tests for data pipelines

**Verification** (`scripts/verification/`):
- Verify model architectures and shapes
- Compare LSTM vs GRU model performance
- Validate data quality and completeness

**Utilities** (`scripts/utilities/`):
- Hyperparameter tuning framework (achieved 25.2% accuracy improvement)
- Performance optimization tools
- Quick fixes and maintenance scripts

### API Endpoints

The application provides REST API endpoints for integration:

- `GET /` - Main dashboard
- `GET /api/current_status` - Current status for all diseases
- `GET /api/forecast/<disease>` - 14-day forecast for specific disease
- `GET /api/climate_data/<disease>` - Climate data for specific disease

Example:
```bash
curl http://localhost:5000/api/forecast/Dengue
```

## Model Architecture

The forecasting system uses both LSTM and GRU neural network architectures:

### LSTM (Long Short-Term Memory)
- **Input Layer**: 30-day sequences of climate and health data (52+ features)
- **LSTM Layers**: Two stacked LSTM layers (64 and 32 units)
- **Dropout**: 0.2 dropout rate for regularization
- **Dense Layers**: Fully connected layers for prediction
- **Output**: Single value (predicted disease cases)

### GRU (Gated Recurrent Unit)
- **Input Layer**: 30-day sequences with comprehensive feature set
- **GRU Layers**: Two stacked GRU layers (64 and 32 units)
- **Dropout**: 0.2 dropout rate
- **Dense Layers**: Fully connected output layers
- **Output**: Predicted case count

### Training Details (Optimized Configuration)

- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: Adam (best performer vs RMSprop, SGD)
- **Learning Rate**: 0.001 (optimal through tuning)
- **Batch Size**: 64 (increased from 32 for better generalization)
- **Epochs**: 100 (increased from 50 for better convergence)
- **Validation Split**: 15% validation, 15% test, 70% training
- **Performance**: 25.2% improvement in Test MAE (0.013288 → 0.009936)
- **R² Score**: Improved from -0.223 to 0.168 (positive correlation achieved)

## Data

The application uses comprehensive historical data with 52+ features:

### Climate Features
- **Temperature**: Min, max, average (°C)
- **Precipitation**: Rainfall patterns (mm)
- **Humidity**: Relative humidity (%)
- **Atmospheric Conditions**: Pressure, wind patterns

### Air Quality
- **PM2.5**: Particulate matter concentration
- **NO2**: Nitrogen dioxide levels
- **Pollutants**: Various air quality indicators

### Environmental Features
- **Vegetation Index (NDVI)**: Land cover and greenness
- **Water Bodies**: Proximity and water quality indicators
- **Land Use**: Urban/rural classification

### Socioeconomic Features
- **Healthcare Access**: Health facility POI counts and distribution
- **Sanitation**: Water access and sanitation POI data
- **Wealth Index**: Relative wealth indicators
- **Infrastructure**: Building density and internet speed

### Health Features
- **Daily Disease Cases**: Historical case counts
- **Temporal Features**: Seasonal patterns, trends

Data sources include CCHAIN climate datasets, OpenStreetMap POI data, geospatial indices, and health surveillance systems.

## Configuration

Edit `config.py` to customize:

- `SEQUENCE_LENGTH`: Number of historical days used for prediction (default: 30)
- `FORECAST_DAYS`: Number of days to forecast ahead (default: 14)
- `DISEASES`: List of diseases to track
- `CLIMATE_FEATURES`: Climate variables to include
- Model paths and other settings

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Deep Learning**: TensorFlow/Keras (LSTM/GRU models)
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly.js (interactive charts)
- **Frontend**: HTML5, CSS3, JavaScript

## Security Considerations

⚠️ **Important**: This application is for educational and demonstration purposes.

- Change the `SECRET_KEY` in production
- Do not use for actual medical decisions without proper validation
- Implement authentication for production deployment
- Validate and sanitize all user inputs
- Use HTTPS in production

## Future Enhancements

- [ ] Real-time data integration from health authorities
- [ ] Mobile-responsive improvements
- [ ] Multi-region support
- [ ] Advanced ensemble models
- [ ] User authentication and role-based access
- [ ] Historical forecast accuracy tracking
- [ ] Export reports (PDF/Excel)
- [ ] SMS/Email alert notifications

## Troubleshooting

**Issue**: TensorFlow installation fails
- **Solution**: Ensure you have compatible Python version (3.8-3.11)
- Try: `pip install tensorflow-cpu` for CPU-only version

**Issue**: Models not loading
- **Solution**: Run `python train_model.py` to generate models

**Issue**: Port 5000 already in use
- **Solution**: Change port in `app.py`: `app.run(port=5001)`

## Contributing

This is an academic project. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is created for educational purposes as part of the Artificial Neural Network course.

## Acknowledgments

- TensorFlow and Keras teams for deep learning frameworks
- Flask community for the web framework
- Plotly for interactive visualizations
- Department of Health, Philippines for disease tracking inspiration

## Contact

For questions or collaborations:
- Ethan Jed Carbonell
- Kirk Henrich Gamo

---

**Disclaimer**: This system is intended for educational and research purposes only. It should not be used as the sole basis for medical or public health decisions. Always consult with healthcare professionals and follow official health guidelines.
