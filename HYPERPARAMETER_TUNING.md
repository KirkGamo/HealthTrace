# Hyperparameter Tuning Documentation

## Overview
This document records the hyperparameter tuning process for the Disease Outbreak Forecasting Neural Network models (LSTM/GRU).

## Current Baseline Configuration

### Optimizer Identified
**Optimizer:** Adam (Adaptive Moment Estimation)
- **Location:** `app/model.py`, line 50
- **Default Learning Rate:** 0.001
- **Default Parameters:**
  - beta_1: 0.9 (exponential decay rate for first moment estimates)
  - beta_2: 0.999 (exponential decay rate for second moment estimates)
  - epsilon: 1e-07

### Current Model Architecture
- **Model Types:** LSTM and GRU
- **First Layer Units:** 64
- **Second Layer Units:** 32
- **Dropout Rate:** 0.2 (20%)
- **Dense Layer Units:** 32
- **Output Layer:** 1 (predicted disease cases)
- **Loss Function:** MSE (Mean Squared Error)
- **Metrics:** MAE (Mean Absolute Error), MSE

### Current Training Configuration
- **Epochs:** 50-100
- **Batch Size:** 32
- **Validation Split:** 20%
- **Early Stopping Patience:** 10-15 epochs
- **Sequence Length:** 30 days

## Hyperparameter Tuning Experiments

### Tuning Strategy
The hyperparameter tuning script (`hyperparameter_tuning.py`) tests 15+ different configurations across multiple dimensions:

#### 1. Optimizer Types
- **Adam** (Current baseline)
- **RMSprop** (Root Mean Square Propagation)
- **SGD** (Stochastic Gradient Descent with momentum)

#### 2. Learning Rates
Testing multiple learning rates for each optimizer:
- 0.01 (10x higher)
- 0.001 (baseline)
- 0.0001 (10x lower)

#### 3. Optimizer-Specific Parameters

**Adam:**
- beta_1: 0.9, 0.95
- beta_2: 0.999

**RMSprop:**
- rho: 0.9, 0.95

**SGD:**
- momentum: 0.0, 0.9
- nesterov: False, True

#### 4. Architecture Parameters
- **LSTM/GRU Units:** 32, 64, 128
- **Dropout Rate:** 0.1, 0.2, 0.3
- **Batch Size:** 16, 32, 64

### Data Splitting Strategy
- **Training Set:** 70% of data
- **Validation Set:** 15% of data (for hyperparameter selection)
- **Test Set:** 15% of data (for final evaluation)
- **Temporal Order:** Preserved (no shuffling)

### Metrics Recorded

For each configuration, the following metrics are recorded:

#### Training Results
- Loss (MSE)
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² Score (Coefficient of Determination)
- Epochs Trained (before early stopping)
- Training Time (seconds)

#### Validation Results
- Loss (MSE)
- MAE
- MSE
- RMSE
- R² Score

#### Test Results
- Loss (MSE)
- MAE
- MSE
- RMSE
- R² Score

### Output Files

The tuning process generates two types of output files:

1. **Detailed JSON File:**
   - Filename: `{disease}_{model_type}_tuning_{timestamp}.json`
   - Contains: Complete configuration, all metrics, training history
   - Location: `hyperparameter_results/`

2. **Summary CSV File:**
   - Filename: `{disease}_{model_type}_summary_{timestamp}.csv`
   - Contains: Tabular summary of all configurations and metrics
   - Location: `hyperparameter_results/`

### Example Configuration Record

```json
{
  "config_id": 1,
  "timestamp": "2025-12-11T10:30:00",
  "disease": "Dengue",
  "model_type": "LSTM",
  
  "configuration": {
    "optimizer": "Adam",
    "learning_rate": 0.001,
    "batch_size": 32,
    "units": 64,
    "dropout": 0.2,
    "epochs": 100,
    "sequence_length": 30
  },
  
  "optimizer_params": {
    "beta_1": 0.9,
    "beta_2": 0.999
  },
  
  "training_results": {
    "loss": 0.045123,
    "mae": 0.156789,
    "rmse": 0.212456,
    "r2_score": 0.876543,
    "epochs_trained": 45,
    "training_time_seconds": 234.56
  },
  
  "validation_results": {
    "loss": 0.052341,
    "mae": 0.167890,
    "rmse": 0.228901,
    "r2_score": 0.854321
  },
  
  "test_results": {
    "loss": 0.049876,
    "mae": 0.163456,
    "rmse": 0.223234,
    "r2_score": 0.865432
  }
}
```

## How to Run Hyperparameter Tuning

### Basic Usage

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run hyperparameter tuning
python hyperparameter_tuning.py
```

### Customize for Different Diseases/Models

Edit `hyperparameter_tuning.py`, line 565:

```python
disease = 'Dengue'  # Options: 'Dengue', 'Typhoid', 'Leptospirosis'
model_type = 'LSTM'  # Options: 'LSTM', 'GRU'
```

### Add More Configurations

Add new configuration dictionaries to the `configurations` list:

```python
configurations.append({
    'optimizer': 'Adam',
    'learning_rate': 0.0005,
    'beta_1': 0.92,
    'beta_2': 0.999,
    'batch_size': 32,
    'units': 64,
    'dropout': 0.25,
    'epochs': 100,
})
```

## Expected Results

### Baseline Performance (Current Configuration)
- **Training MAE:** ~0.15-0.25
- **Validation MAE:** ~0.16-0.28
- **Test MAE:** ~0.16-0.27
- **R² Score:** ~0.85-0.90

### Optimization Goals
- Minimize Test MAE (primary metric)
- Maximize Test R² Score
- Balance between training time and performance
- Avoid overfitting (training metrics >> validation/test metrics)

## Analysis Guidelines

### Comparing Results

1. **Sort by Test MAE** (lower is better)
2. **Check for overfitting:**
   - Training MAE << Validation/Test MAE = overfitting
   - Consider higher dropout or regularization

3. **Validate generalization:**
   - Validation and Test metrics should be similar
   - Large difference indicates poor generalization

4. **Consider training efficiency:**
   - Training time vs. performance trade-off
   - Epochs trained (early stopping indicates convergence)

### Best Configuration Selection

The best configuration is selected based on:
1. **Lowest Test MAE** (primary criterion)
2. **Highest Test R² Score**
3. **Good generalization** (Train ≈ Val ≈ Test)
4. **Reasonable training time**

## Implementation Notes

### Technical Details

1. **Data Preprocessing:**
   - All features scaled using MinMaxScaler
   - Temporal sequences of 30 days
   - No data shuffling (preserves temporal order)

2. **Model Architecture:**
   - Two-layer LSTM/GRU with dropout
   - Dense layer with ReLU activation
   - Single output node for case prediction

3. **Training Process:**
   - Early stopping on validation loss
   - Best weights restoration
   - Verbose logging for monitoring

4. **Evaluation:**
   - Separate test set (never seen during training)
   - Multiple metrics for comprehensive assessment
   - Training history saved for analysis

### Reproducibility

- Set random seeds for reproducibility:
  ```python
  import numpy as np
  import tensorflow as tf
  np.random.seed(42)
  tf.random.set_seed(42)
  ```

- Results may vary slightly due to:
  - Random weight initialization
  - GPU non-deterministic operations
  - Data preprocessing variations

## Next Steps

After hyperparameter tuning:

1. **Select Best Configuration:**
   - Review summary CSV/JSON files
   - Analyze performance metrics
   - Consider computational constraints

2. **Update Model:**
   - Modify `app/model.py` with best configuration
   - Update `train_model.py` parameters
   - Retrain models with optimal settings

3. **Validate on Production:**
   - Test with real-world data
   - Monitor performance over time
   - Iterate as needed

## References

- **Adam Optimizer:** Kingma & Ba (2014) - "Adam: A Method for Stochastic Optimization"
- **RMSprop:** Hinton et al. (2012) - Coursera Lecture
- **SGD with Momentum:** Rumelhart et al. (1986)
- **LSTM:** Hochreiter & Schmidhuber (1997)
- **GRU:** Cho et al. (2014)

---

**Document Version:** 1.0  
**Last Updated:** December 11, 2025  
**Author:** HealthTrace Development Team
