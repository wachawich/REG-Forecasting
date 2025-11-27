# REG-Forecasting

A machine learning-based forecasting system for renewable energy (Solar and Wind) prediction using LSTM and GRU deep learning models.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Pipeline](#data-pipeline)
  - [Server API](#server-api)
  - [Jupyter Notebooks](#jupyter-notebooks)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

REG-Forecasting is a comprehensive system for predicting renewable energy generation (solar and wind power). It uses:

- **LSTM (Long Short-Term Memory)** - For sequence-to-sequence forecasting
- **GRU (Gated Recurrent Unit)** - For efficient temporal modeling
- **Apache Airflow** - For pipeline orchestration and scheduling
- **Flask API** - For serving predictions in real-time
- **DuckDB** - For efficient data management and queries

The system automatically fetches weather data, processes it, trains/retrains models, and provides forecasting through a REST API.

## 📁 Project Structure

```
REG-Forecasting/
├── jupyter/                              # Jupyter notebooks for data science
│   ├── DataEngineering/
│   │   ├── state_1_historical_data/     # Historical data processing
│   │   │   └── historical_data_v2_main.ipynb
│   │   └── state_3_retrain_data/        # Daily retraining data prep
│   │       └── historical_data_daily_retrain.ipynb
│   └── DataScience/
│       ├── GRU/                         # GRU model experiments
│       │   ├── GRU_Solar.ipynb
│       │   └── GRU_Wind.ipynb
│       └── LSTM/                        # LSTM model experiments
│           ├── LSTM__solar.ipynb
│           └── LSTM_wind.ipynb
│
├── pipeline/                             # Airflow pipeline orchestration
│   ├── dags/                            # Airflow DAGs
│   │   ├── call_retrain_data_pipeline_gru.py
│   │   ├── call_retrain_data_pipeline_lstm.py
│   │   ├── forecast_pipeline_gru.py
│   │   └── forecast_pipeline_lstm.py
│   ├── db/                              # Database utilities
│   │   ├── call_api.py
│   │   ├── duckdbcon.py
│   │   └── helper.py
│   ├── functions/                       # Data processing functions
│   │   ├── electic.py
│   │   ├── merge_df.py
│   │   ├── seasonal.py
│   │   ├── variable.py
│   │   └── weather.py
│   ├── jobs/                            # Individual pipeline tasks
│   │   ├── fetch_retrain_data.py
│   │   ├── fetch_weather.py
│   │   ├── load_to_duckdb.py
│   │   ├── compare_accuracy_overtime.py
│   │   ├── re_predict_data_gru.py
│   │   ├── re_predict_data_lstm.py
│   │   ├── store_retrain_data.py
│   │   ├── weather_predict_gru.py
│   │   └── weather_predict_lstm.py
│   ├── docker-compose.yml
│   ├── Dockerfile.airflow
│   └── requirements.txt
│
├── server/                               # Flask prediction server
│   ├── server.py                        # Main Flask application
│   ├── db/                              # Database helpers
│   │   ├── duckdbcon.py
│   │   └── helper.py
│   ├── logic/                           # Model prediction logic
│   │   ├── gru_solar.py
│   │   ├── gru.py
│   │   ├── retrain_data.py
│   │   ├── solar_gru.py
│   │   ├── solar_lstm.py
│   │   ├── wind_gru.py
│   │   └── wind_lstm.py
│   ├── model/                           # Pre-trained model weights
│   │   ├── variable.py
│   │   ├── weight_gru/
│   │   │   ├── Solar/
│   │   │   │   └── solar_gru_weights_final.pth
│   │   │   └── Wind/
│   │   │       └── Wind_gru_weights_final.pth
│   │   └── weights_lstm/
│   │       ├── solar/
│   │       │   ├── solar_lstm_model.keras
│   │       │   ├── solar_scaler_x.joblib
│   │       │   └── solar_scaler_y.joblib
│   │       └── wind/
│   │           ├── wind_lstm_model.keras
│   │           ├── wind_scaler_x.joblib
│   │           └── wind_scaler_y.joblib
│   ├── nginx/                           # Nginx reverse proxy config
│   │   └── conf.d/
│   │       └── default.conf
│   ├── docker-compose.yml
│   ├── Dockerfile.server
│   └── requirements.txt
│
├── LICENSE
└── README.md
```

## ✨ Features

- **Dual Model Support**: LSTM and GRU architectures for comparison
- **Multi-Target Forecasting**: Solar and Wind energy predictions
- **Automated Data Pipeline**: 
  - Weather data fetching
  - Data preprocessing and normalization
  - Database storage and retrieval
- **Periodic Model Retraining**: Automatic model updates with new data
- **Real-Time API**: Flask REST API for serving predictions
- **Performance Monitoring**: Accuracy tracking over time
- **Docker Containerization**: Easy deployment and scalability
- **Swagger Documentation**: Interactive API documentation

## 🛠️ Tech Stack

**Backend & ML:**
- Python 3.x
- TensorFlow/Keras (LSTM models)
- PyTorch (GRU models)
- scikit-learn (preprocessing and evaluation)

**Data Processing:**
- pandas
- NumPy
- pyarrow
- DuckDB

**Orchestration & Serving:**
- Apache Airflow (workflow orchestration)
- Flask (REST API framework)
- Flask-CORS (Cross-origin resource sharing)
- Gunicorn (production server)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (reverse proxy)

**Utilities:**
- joblib (model persistence)
- python-dotenv (environment configuration)
- requests (API calls)
- flasgger (Swagger UI)

## 📦 Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Git
- 4GB+ RAM
- CUDA GPU (optional, for faster training)

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/wachawich/REG-Forecasting.git
cd REG-Forecasting
```

### 2. Install Dependencies (Local Development)

**For Pipeline:**
```bash
cd pipeline
pip install -r requirements.txt
```

**For Server:**
```bash
cd ../server
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `server` directory:

```env
# Database
DATABASE_PATH=./duckdb.db

# API
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# CUDA (optional)
CUDA_VISIBLE_DEVICES=-1
```

## 💻 Usage

### Data Pipeline

The pipeline automatically executes on a daily schedule using Airflow. It follows this flow:

1. **Fetch Weather Data** → API calls to weather services
2. **Data Preprocessing** → Cleaning, normalization, feature engineering
3. **Model Prediction** → Generate forecasts using trained models
4. **Store Results** → Save to DuckDB

**Available Pipelines:**
- `forecast_pipeline_gru.py` - GRU-based forecasting
- `forecast_pipeline_lstm.py` - LSTM-based forecasting
- `call_retrain_data_pipeline_gru.py` - GRU model retraining
- `call_retrain_data_pipeline_lstm.py` - LSTM model retraining

### Server API

**Start the Flask server:**

```bash
cd server
python server.py
```

The API will be available at `http://localhost:5000`

**Swagger Documentation:** `http://localhost:5000/apidocs/`

### Jupyter Notebooks

**Data Engineering:**
- `jupyter/DataEngineering/state_1_historical_data/historical_data_v2_main.ipynb` - Process historical data
- `jupyter/DataEngineering/state_3_retrain_data/historical_data_daily_retrain.ipynb` - Prepare daily retrain data

**Data Science:**
- `jupyter/DataScience/GRU/GRU_Solar.ipynb` - Develop and test GRU for Solar
- `jupyter/DataScience/GRU/GRU_Wind.ipynb` - Develop and test GRU for Wind
- `jupyter/DataScience/LSTM/LSTM__solar.ipynb` - Develop and test LSTM for Solar
- `jupyter/DataScience/LSTM/LSTM_wind.ipynb` - Develop and test LSTM for Wind

## 🔌 API Endpoints

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check / Welcome message |

### Solar Predictions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/solar_gru_predict` | Predict solar energy using GRU |
| POST | `/api/v1/solar_lstm_predict` | Predict solar energy using LSTM |

**Solar Request Example:**
```json
{
  "data": [
    {
      "value": 1.14,
      "temp": 29.1,
      "humidity": 70
    },
    {
      "value": 1.20,
      "temp": 29.3,
      "humidity": 72
    }
  ]
}
```

### Wind Predictions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/wind_gru_predict` | Predict wind energy using GRU |
| POST | `/api/v1/wind_lstm_predict` | Predict wind energy using LSTM |

**Wind Request Example:**
```json
{
  "data": [
    {
      "value": 2.34,
      "wind_speed": 3.6,
      "wind_dir": 110
    },
    {
      "value": 2.45,
      "wind_speed": 3.7,
      "wind_dir": 112
    }
  ]
}
```

### Data Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/retrain_data.get` | Retrieve retraining dataset |

**Retrain Data Request:**
```json
{
  "date": "2025-11-27"
}
```

## 🤖 Models

### LSTM Models

- **solar_lstm_model.keras** - Solar power prediction
  - Input features: Temperature, Humidity, Solar Radiation, etc.
  - Sequence length: Configured via `SEQUENCE_LEGHTH` variable
  - Scalers: `solar_scaler_x.joblib`, `solar_scaler_y.joblib`

- **wind_lstm_model.keras** - Wind power prediction
  - Input features: Wind Speed, Wind Direction, etc.
  - Sequence length: Configured via `SEQUENCE_LEGHTH` variable
  - Scalers: `wind_scaler_x.joblib`, `wind_scaler_y.joblib`

### GRU Models

- **solar_gru_weights_final.pth** - Solar power prediction (PyTorch)
- **Wind_gru_weights_final.pth** - Wind power prediction (PyTorch)

### Model Features

Configuration in `server/model/variable.py`:

- `FEATURE_COLS_LSTM_SOLAR` - Feature columns for LSTM solar model
- `FEATURE_COLS_LSTM_WIND` - Feature columns for LSTM wind model
- `FEATURE_COLS_GRU_SOLAR` - Feature columns for GRU solar model
- `FEATURE_COLS_GRU_WIND` - Feature columns for GRU wind model
- `SEQUENCE_LEGHTH` - Input sequence length for temporal models

## ⚙️ Configuration

### Environment Variables

**server/.env:**
```env
DATABASE_PATH=./duckdb.db
FLASK_ENV=production
PORT=5000
CUDA_VISIBLE_DEVICES=-1
```

### Database

DuckDB is used for efficient data management. Connection configured in:
- `server/db/duckdbcon.py` - Server-side database connection
- `pipeline/db/duckdbcon.py` - Pipeline-side database connection

### Nginx Configuration

Reverse proxy configured in `server/nginx/conf.d/default.conf`

## 🐳 Docker Deployment

### Pipeline (Airflow)

```bash
cd pipeline
docker-compose up -d
```

**Services:**
- Apache Airflow Scheduler
- Apache Airflow Webserver (http://localhost:8080)
- PostgreSQL (Airflow metadata)

### Server

```bash
cd server
docker-compose up -d
```

**Services:**
- Flask API Server
- Nginx Reverse Proxy (http://localhost:80)
- DuckDB Database

### Full Deployment

```bash
# Pipeline
cd pipeline && docker-compose up -d && cd ..

# Server
cd server && docker-compose up -d && cd ..
```

View logs:
```bash
docker-compose logs -f
```

Stop all services:
```bash
docker-compose down
```

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

---

**Project Owner:** wachawich  
**Repository:** [REG-Forecasting](https://github.com/wachawich/REG-Forecasting)  
**Last Updated:** November 2025
