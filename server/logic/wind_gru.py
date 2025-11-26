import numpy as np
import joblib
import torch
from gru import GRUModel

def predict_wind_gru(input_df, model_path, scaler_x_path, scaler_y_path, feature_cols, window_size, device="cpu", target_col="value"):

    df_wind_test = input_df.copy().reset_index(drop=True)

    input_size = len(feature_cols)
    hidden_size = 64
    num_layers = 2

    loaded_wind_model = GRUModel(input_size, hidden_size, num_layers)

    loaded_state_dict = torch.load(model_path, map_location=device)
    loaded_wind_model.load_state_dict(loaded_state_dict)

    loaded_wind_model.to(device)
    loaded_wind_model.eval()

    x_scaler = joblib.load(scaler_x_path)
    y_scaler = joblib.load(scaler_y_path)

    X_raw = df_wind_test[feature_cols].astype(float).values
    X_scaled = x_scaler.transform(X_raw)

    X_list = []
    for i in range(len(X_scaled) - window_size):
        X_list.append(X_scaled[i:i+window_size])

    if len(X_list) == 0:
        df_wind_test[target_col] = np.nan
        return df_wind_test

    X_array = np.array(X_list)
    X_tensor = torch.tensor(X_array, dtype=torch.float32).to(device)

    preds_list = []
    with torch.no_grad():
        for i in range(len(X_tensor)):
            y_pred = loaded_wind_model(X_tensor[i:i+1])
            preds_list.append(y_pred.cpu().numpy())

    preds_scaled = np.concatenate(preds_list, axis=0)
    preds_real = y_scaler.inverse_transform(preds_scaled).flatten()

    df_wind_test[target_col] = np.nan

    start_idx = window_size
    end_idx = window_size + len(preds_real)

    df_wind_test.loc[start_idx : end_idx - 1, target_col] = preds_real

    return df_wind_test
