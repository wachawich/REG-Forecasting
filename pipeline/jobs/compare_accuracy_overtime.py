import pandas as pd
import numpy as np
from db.duckdbcon import get_duckdb_connection

def accuracy_overtime(actual, pred, threshold=100, smooth_window=None):

    actual = list(actual)
    pred   = list(pred)

    if smooth_window is not None and smooth_window > 1:
        actual = pd.Series(actual).rolling(
            smooth_window, center=True, min_periods=1
        ).mean().values
        pred   = pd.Series(pred).rolling(
            smooth_window, center=True, min_periods=1
        ).mean().values

    actual_diff = np.diff(actual)
    pred_diff   = np.diff(pred)

    def to_dir(d):
        d = np.where(np.abs(d) < threshold, 0, d)
        return np.sign(d)

    actual_dir = to_dir(actual_diff)
    pred_dir   = to_dir(pred_diff)

    correct = np.sum(actual_dir == pred_dir)
    total   = len(actual_dir)
    acc     = correct / total if total > 0 else 0
    return acc * 100, actual_dir, pred_dir

def store_to_compare_db():
    
    data_actual = pd.read_parquet("/opt/airflow/shared/tmp_retrain_weather.parquet")
    data_repredict_solar = pd.read_parquet("/opt/airflow/shared/re_predict_weather_solar.parquet")
    data_repredict_wind = pd.read_parquet("/opt/airflow/shared/re_predict_weather_wind.parquet")
    
    df_actual = pd.DataFrame(data_actual)
    df_actual_solar = df_actual[df_actual['type-name'] == 'Solar']
    df_actual_wind  = df_actual[df_actual['type-name'] == 'Wind']
    
    df_repredict_solar = pd.DataFrame(data_repredict_solar)
    df_repredict_wind = pd.DataFrame(data_repredict_wind)
    
    print(df_repredict_solar.shape)
    print(df_repredict_wind.shape)
    print(df_actual_solar.shape)
    print(df_actual_wind.shape) 
    
    solar_acc, solar_actual_dir, solar_pred_dir = accuracy_overtime(
        df_actual_solar["value"],
        df_repredict_solar["value"],
        threshold=100,
        smooth_window=5
    )
    
    wind_acc, wind_actual_dir, wind_pred_dir = accuracy_overtime(
        df_actual_wind["value"],
        df_repredict_wind["value"],
        threshold=100,
        smooth_window=5
    )
    
    unique_dates = df_actual_solar['date'].unique()

    compare_df_solar = pd.DataFrame({
        "date": unique_dates,
        "type-name": "Solar",
        "accuracy_overtime": solar_acc
    })
    
    compare_df_wind = pd.DataFrame({
        "date": unique_dates,
        "type-name": "Wind",
        "accuracy_overtime": wind_acc
    })
    
    
    con = get_duckdb_connection()
    
    # # Insert data
    con.execute("""
        INSERT INTO accuracy_overtime_solar
        SELECT * FROM compare_df_solar
    """)

    con.execute("""
        INSERT INTO accuracy_overtime_wind
        SELECT * FROM compare_df_wind
    """)
    
    print("Data loaded retrain data into DuckDB successfully.")

store_to_compare_db()
