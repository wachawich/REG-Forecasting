import pandas as pd
from db.call_api import call_api
from dotenv import load_dotenv
import os
from db.helper import  get_today, get_today_minus_3, get_max_retrain_date


load_dotenv("/opt/airflow/.env")

def predict_solar(bodys, start_date):
    urls = os.getenv("BASE_URL") + os.getenv("BASE_PATH") + "solar_gru_predict"
    
    res = call_api(
        url=urls,
        body=bodys,
        method="POST",
    )
    
    df_res = pd.DataFrame(res['prediction'])
    today = get_today()
    
    df_res = df_res[df_res['date'] >= start_date]
    
    df_res['predict_date'] = today
    df_res.to_parquet("/opt/airflow/shared/re_predict_weather_solar.parquet")
    
def predict_wind(bodys, start_date):
    urls = os.getenv("BASE_URL") + os.getenv("BASE_PATH") + "wind_gru_predict"
    
    res = call_api(
        url=urls,
        body=bodys,
        method="POST",
    )
    
    df_res = pd.DataFrame(res['prediction'])
    today = get_today()
    
    df_res = df_res[df_res['date'] >= start_date]
    
    df_res['predict_date'] = today
    df_res.to_parquet("/opt/airflow/shared/re_predict_weather_wind.parquet")
    
def re_predict_weather():
    
    data = pd.read_parquet("/opt/airflow/shared/tmp_repredict_weather.parquet")
    data_retrain = pd.read_parquet("/opt/airflow/shared/tmp_retrain_weather.parquet")
    df = pd.DataFrame(data)
    df_retrain = pd.DataFrame(data_retrain)
    
    if df_retrain.empty:
        print("⚠️ df_retrain is empty → skip prediction")
        return

    if "date" not in df_retrain.columns:
        print("⚠️ df_retrain has no 'date' column → skip prediction")
        return

    if df_retrain["date"].isna().all():
        print("⚠️ df_retrain['date'] is all NaN → skip prediction")
        return
    
    start_date = df_retrain["date"].min()
    
    df_solar = df[df['type-name'] == 'Solar']
    df_wind  = df[df['type-name'] == 'Wind']
    
    df_solar = df_solar.reset_index(drop=True)
    df_wind = df_wind.reset_index(drop=True)   
    
    body_solar = {
        "data": df_solar.to_dict(orient="records")
    }
    
    body_wind = {
        "data": df_wind.to_dict(orient="records")
    }
    
    predict_solar(body_solar, start_date)
    predict_wind(body_wind, start_date)

re_predict_weather()
