from flask import Flask, jsonify, request
from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
import os
import numpy as np
from flask_cors import CORS

from logic.gru_solar import solar_gru_prediction
from logic.retrain_data import get_retrain_data
from logic.solar_lstm import predict_solar_lstm
from logic.wind_lstm import predict_wind_lstm
from logic.solar_gru import predict_solar_gru
from logic.wind_gru import predict_wind_gru
from model.variable import FEATURE_COLS_LSTM_SOLAR, FEATURE_COLS_LSTM_WIND, FEATURE_COLS_GRU_SOLAR, FEATURE_COLS_GRU_WIND, SEQUENCE_LEGHTH

import pandas as pd

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)
CORS(app, supports_credentials=True)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True, 
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

base_path = "/api/v1"

load_dotenv() 

@app.route("/")
def home():
    """
    Home API
    ---
    tags:
      - System
    summary: Welcome message
    responses:
      200:
        description: API is running
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Welcome to Flask API with DuckDB!"
    """
    return jsonify({"message": "Welcome to Flask API with DuckDB!"})


# # Model Prediction
# ----------------- SOLAR GRU PREDICT -----------------
@app.route(f"/{base_path}/solar_gru_predict", methods=["POST"])
def solar_gru_predict():
    """
    Solar GRU Prediction API
    ---
    tags:
      - Solar GRU
    summary: Predict solar data using GRU model
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: array
          items:
            type: object
          example:
            - value: 1.23
              feature1: 0.5
              feature2: 0.8
            - value: 1.30
              feature1: 0.6
              feature2: 0.82
    responses:
      200:
        description: Prediction results
        schema:
          type: object
          properties:
            prediction:
              type: array
              items:
                type: object
    """
    data = request.get_json()
    df = pd.DataFrame(data)
    
    print("solar_gru_predict", df)

    df_preds = predict_solar_gru(
        input_df=df,
        model_path="./model/weight_gru/Solar/solar_gru_weights_final.pth",
        scaler_x_path="./model/weight_gru/Solar/x_scaler.pkl",
        scaler_y_path="./model/weight_gru/Solar/y_scaler.pkl",
        feature_cols=FEATURE_COLS_GRU_SOLAR,
        window_size=48,
        device="cpu",
        target_col="value"
    )

    return jsonify({"prediction": df_preds.to_dict(orient="records")})


# ----------------- WIND GRU PREDICT -----------------
@app.route(f"/{base_path}/wind_gru_predict", methods=["POST"])
def wind_gru_predict():
    """
    Wind GRU Prediction API
    ---
    tags:
      - Wind GRU
    summary: Predict wind data using GRU model
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: array
          items:
            type: object
          example:
            - value: 2.10
              wind_speed: 3.4
              wind_dir: 120
            - value: 2.20
              wind_speed: 3.5
              wind_dir: 125
    responses:
      200:
        description: Prediction results
        schema:
          type: object
          properties:
            prediction:
              type: array
              items:
                type: object
    """
    data = request.get_json()
    df = pd.DataFrame(data)

    df_preds = predict_wind_gru(
        input_df=df,
        model_path="./model/weight_gru/Wind/Wind_gru_weights_final.pth",
        scaler_x_path="./model/weight_gru/Wind/wind_x_scaler.pkl",
        scaler_y_path="./model/weight_gru/Wind/wind_y_scaler.pkl",
        feature_cols=FEATURE_COLS_GRU_WIND,
        window_size=48,
        device="cpu",
        target_col="value"
    )

    return jsonify({"prediction": df_preds.to_dict(orient="records")})


# ----------------- SOLAR LSTM PREDICT -----------------
@app.route(f"/{base_path}/solar_lstm_predict", methods=["POST"])
def solar_lstm_predict():
    """
    Solar LSTM Prediction API
    ---
    tags:
      - Solar LSTM
    summary: Predict solar forecasting using LSTM model
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
              example:
                - value: 1.14
                  temp: 29.1
                  humidity: 70
                - value: 1.20
                  temp: 29.3
                  humidity: 72
    responses:
      200:
        description: LSTM prediction output
        schema:
          type: object
          properties:
            prediction:
              type: array
              items:
                type: object
    """
    data = request.get_json()
    df_test = pd.DataFrame(data["data"])

    df_pred = predict_solar_lstm(
        input_df=df_test,
        df_test=df_test,
        model_path="./model/weights_lstm/solar/solar_lstm_model.keras",
        scaler_x_path="./model/weights_lstm/solar/solar_scaler_x.joblib",
        scaler_y_path="./model/weights_lstm/solar/solar_scaler_y.joblib",
        feature_cols=FEATURE_COLS_LSTM_SOLAR,
        seq_length=SEQUENCE_LEGHTH,
        target_col="value"
    )

    return jsonify({"prediction": df_pred.to_dict(orient="records")})


# ----------------- WIND LSTM PREDICT -----------------
@app.route(f"/{base_path}/wind_lstm_predict", methods=["POST"])
def wind_lstm_predict():
    """
    Wind LSTM Prediction API
    ---
    tags:
      - Wind LSTM
    summary: Predict wind forecasting using LSTM model
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
              example:
                - value: 2.34
                  wind_speed: 3.6
                  wind_dir: 110
                - value: 2.45
                  wind_speed: 3.7
                  wind_dir: 112
    responses:
      200:
        description: LSTM prediction output
        schema:
          type: object
          properties:
            prediction:
              type: array
              items:
                type: object
    """
    data = request.get_json()
    df_test = pd.DataFrame(data["data"])

    df_pred = predict_wind_lstm(
        input_df=df_test,
        df_test=df_test,
        model_path="./model/weights_lstm/wind/wind_lstm_model.keras",
        scaler_x_path="./model/weights_lstm/wind/wind_scaler_x.joblib",
        scaler_y_path="./model/weights_lstm/wind/wind_scaler_y.joblib",
        feature_cols=FEATURE_COLS_LSTM_WIND,
        seq_length=SEQUENCE_LEGHTH,
        target_col="value"
    )

    return jsonify({"prediction": df_pred.to_dict(orient="records")})

# # Forecast reult DB
# @app.route(f"/{base_path}/fore_result.get", methods=["GET"])
# def get_forcast_data():
    
#     data = request.json
    
#     input_date = data['date']
    
#     return "sima"


# # Real result DB (retrain data)
# ----------------- RETRAIN DATA -----------------
@app.route(f"/{base_path}/retrain_data.get", methods=['POST'])
def get_retrains_data():
    """
    Retrain Data API
    ---
    tags:
      - Retrain Data
    summary: Get retraining dataset for models
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          example:
            date: "2025-11-27"
    responses:
      200:
        description: Retrain data result
    """
    print(request.json)
    result = get_retrain_data(request.json)
    return result

# # Accuracy Overtime DB
# @app.route("/callJson", methods=["POST"])
# def callJsonAI():
#     return callJsonAPI()


if __name__ == "__main__":
    app.run(debug=True)