# HealthTrace - Disease Outbreak Forecasting System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange)

A Python-based web application to forecast disease outbreaks in the Philippines using deep learning models (LSTM/GRU) with TensorFlow. The application processes historical climate and health data to predict future disease incidence and provides an interactive dashboard for public health officials.

**Course:** Artificial Neural Network  
**Authors:** Ethan Jed Carbonell and Kirk Henrich Gamo

## Features

- 🤖 **Deep Learning Models**: LSTM/GRU neural networks for time-series forecasting
- 📊 **Interactive Dashboard**: Real-time visualization of disease forecasts and trends
- 🌡️ **Climate Integration**: Correlates climate factors (temperature, humidity, rainfall) with disease patterns
- ⚠️ **Early Warning System**: Alert levels based on predicted outbreak severity
- 🏥 **Multi-Disease Support**: Tracks Dengue, Influenza, Typhoid, and Malaria
- 📈 **14-Day Forecasts**: Predicts disease cases two weeks in advance

## Project Structure

```
HealthTrace/
├── app/
│   ├── data/                    # Historical climate and health data
│   ├── models/                  # Trained LSTM/GRU models
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Dashboard styling
│   │   └── js/
│   │       └── dashboard.js    # Frontend JavaScript
│   ├── templates/
│   │   └── index.html          # Main dashboard template
│   ├── data_utils.py           # Data processing utilities
│   └── model.py                # LSTM/GRU model implementation
├── app.py                      # Flask backend application
├── config.py                   # Configuration settings
├── train_model.py             # Model training script
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
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
2. **Select a Disease**: Click on any disease button (Dengue, Influenza, Typhoid, Malaria)
3. **View Forecasts**: See 14-day predictions with historical context
4. **Monitor Alerts**: Check alert levels (LOW, MEDIUM, HIGH) based on predictions
5. **Analyze Climate**: View climate factors affecting disease patterns

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

The forecasting system uses LSTM (Long Short-Term Memory) neural networks:

- **Input Layer**: 30-day sequences of climate and health data
- **LSTM Layers**: Two stacked LSTM layers (64 and 32 units)
- **Dropout**: 0.2 dropout rate for regularization
- **Dense Layers**: Fully connected layers for prediction
- **Output**: Single value (predicted disease cases)

### Training Details

- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: Adam
- **Batch Size**: 32
- **Epochs**: 50 (with early stopping)
- **Validation Split**: 20%

## Data

The application uses historical data with the following features:

- **Climate Features**:
  - Temperature (°C)
  - Humidity (%)
  - Rainfall (mm)

- **Health Features**:
  - Daily disease cases

Sample data is automatically generated for demonstration purposes, simulating realistic patterns for the Philippines climate and disease trends.

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
