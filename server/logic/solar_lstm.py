import numpy as np
import joblib
from tensorflow.keras.models import load_model

def predict_solar_lstm(
    input_df,
    df_test,
    model_path="solar_lstm_model.keras",
    scaler_x_path="solar_scaler_x.joblib",
    scaler_y_path="solar_scaler_y.joblib",
    feature_cols=None,
    seq_length=24,
    target_col="SOLAR"
):
    df_test_local = input_df.copy().reset_index(drop=True)

    model = load_model(model_path)
    scaler_x = joblib.load(scaler_x_path)
    scaler_y = joblib.load(scaler_y_path)

    df_test_local["sunrise_min"] = (
        df_test_local["sunrise_time_h"] * 60 + df_test_local["sunrise_time_m"]
    )
    df_test_local["sunset_min"] = (
        df_test_local["sunset_time_h"] * 60 + df_test_local["sunset_time_m"]
    )
    df_test_local["time_min"] = df_test_local["time"] * 60

    df_test_local["is_night"] = (
        (df_test_local["time_min"] < df_test_local["sunrise_min"]) |
        (df_test_local["time_min"] > df_test_local["sunset_min"])
    ).astype(int)

    feature_cols_all = feature_cols + ["is_night"]

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
            f"จำนวนแถวใน CSV น้อยกว่า seq_length ({seq_length}) "
            "เลยสร้าง sequence ไม่ได้"
        )

    pred_scaled = model.predict(X_test_seq)
    pred = scaler_y.inverse_transform(pred_scaled)
    pred_flat = pred.flatten()

    df_out = df_test.copy().reset_index(drop=True)
    df_out[target_col] = np.nan
    start_idx = seq_length
    end_idx = seq_length + len(pred_flat)

    df_out.loc[start_idx:end_idx - 1, target_col] = pred_flat

    return df_out