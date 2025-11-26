from flask import Flask, jsonify, request
from flask import Flask
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

base_path = "/api/v1"

load_dotenv() 

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Flask API with DuckDB!"})


# # Model Prediction
@app.route(f"/{base_path}/solar_gru_predict", methods=["POST"])
def solar_gru_predict():
    
    data = request.get_json()
    df = pd.DataFrame(data)

    df_preds = predict_solar_gru(
        input_df=df,
        model_path="Wind_gru_weights_final.pth",
        scaler_x_path="wind_x_scaler.pkl",
        scaler_y_path="wind_y_scaler.pkl",
        feature_cols=FEATURE_COLS_GRU_SOLAR,
        window_size=48,
        device="cpu",
        target_col="value"
    )

    return jsonify({"prediction": df_preds.to_dict(orient="records")})

@app.route(f"/{base_path}/wind_gru_predict", methods=["POST"])
def wind_gru_predict():
    
    data = request.get_json()
    df = pd.DataFrame(data)

    df_preds = predict_wind_gru(
        input_df=df,
        model_path="Wind_gru_weights_final.pth",
        scaler_x_path="wind_x_scaler.pkl",
        scaler_y_path="wind_y_scaler.pkl",
        feature_cols=FEATURE_COLS_GRU_SOLAR,
        window_size=48,
        device="cpu",
        target_col="value"
    )

    return jsonify({"prediction": df_preds.to_dict(orient="records")})


@app.route(f"/{base_path}/solar_lstm_predict", methods=["POST"])
def solar_lstm_predict():

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

@app.route(f"/{base_path}/wind_lstm_predict", methods=["POST"])
def wind_lstm_predict():

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
# @app.route("f"/{base_path}/fore_result.get", methods=["GET"])
# def processUserInfoJson():
#     return processFunction(model)


# # Real result DB (retrain data)
@app.route(f"/{base_path}/retrain_data.get", methods=['POST'])
def get_retrains_data():
    print(request.json)
    result = get_retrain_data(request.json)
    return result

# # Accuracy Overtime DB
# @app.route("/callJson", methods=["POST"])
# def callJsonAI():
#     return callJsonAPI()


if __name__ == "__main__":
    app.run(debug=True)