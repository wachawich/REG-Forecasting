import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import os

def predict_wind(
    input_df,
    df_test,
    model_path,
    scaler_x_path,
    scaler_y_path,
    feature_cols,
    seq_length=24,
    target_col="value"
):
    df_test_local = input_df.copy().reset_index(drop=True)

    model = load_model(model_path)
    scaler_x = joblib.load(scaler_x_path)
    scaler_y = joblib.load(scaler_y_path)

    if target_col not in df_test_local.columns:
        df_test_local[target_col] = 0.0

    for i in [1, 2, 3]:
        df_test_local[f"value_lag{i}"] = df_test_local[target_col].shift(i).fillna(0)

    lag_cols = ["value_lag1", "value_lag2", "value_lag3"]

    feature_cols_all = feature_cols + lag_cols

    X_test_raw = df_test_local[feature_cols_all].values.astype(float)

    X_test_scaled = scaler_x.transform(X_test_raw)

    def make_sequences_for_inference(X_scaled, seq_length):
        X_seq = []
        for i in range(len(X_scaled) - seq_length):
            X_seq.append(X_scaled[i : i + seq_length])
        return np.array(X_seq, dtype="float32")

    X_test_seq = make_sequences_for_inference(X_test_scaled, seq_length)

    if len(X_test_seq) == 0:
        raise ValueError(
            f"จำนวนแถวของ CSV < seq_length ({seq_length}) ทำให้สร้าง sequence ไม่ได้"
        )

    pred_scaled = model.predict(X_test_seq)
    pred = scaler_y.inverse_transform(pred_scaled)
    pred_flat = pred.flatten()

    df_out = input_df.copy().reset_index(drop=True)
    df_out[target_col] = np.nan
    start_idx = seq_length
    end_idx = seq_length + len(pred_flat)

    df_out.loc[start_idx:end_idx - 1, target_col] = pred_flat

    return df_out
