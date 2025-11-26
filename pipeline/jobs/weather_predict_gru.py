import pandas as pd
from db.call_api import call_api
from dotenv import load_dotenv
import os
from db.helper import  get_today
from db.helper import get_today_minus_3

load_dotenv("/opt/airflow/.env")

def predict_solar(bodys):
    urls = os.getenv("BASE_URL") + os.getenv("BASE_PATH") + "solar_gru_predict"
    
    res = call_api(
        url=urls,
        body=bodys,
        method="POST",
    )
    
    df_res = pd.DataFrame(res['prediction'])
    today = get_today()
    
    df_res['predict_date'] = today
    
    date_cut = get_today_minus_3()
    df_res = df_res[df_res['date'] > date_cut]
    
    df_res.to_parquet("/opt/airflow/shared/predict_weather_forecast_solar.parquet")
    
def predict_wind(bodys):
    urls = os.getenv("BASE_URL") + os.getenv("BASE_PATH") + "wind_gru_predict"
    
    res = call_api(
        url=urls,
        body=bodys,
        method="POST",
    )
    
    df_res = pd.DataFrame(res['prediction'])
    today = get_today()
    
    df_res['predict_date'] = today
    
    date_cut = get_today_minus_3()
    df_res = df_res[df_res['date'] > date_cut]
    
    df_res.to_parquet("/opt/airflow/shared/predict_weather_forecast_wind.parquet")
    
def predict_weather():
    
    data = pd.read_parquet("/opt/airflow/shared/tmp_weather.parquet")
    df = pd.DataFrame(data)
    bodys = {
        "data": df.to_dict(orient="records")
    }
    
    predict_solar(bodys)
    predict_wind(bodys)

predict_weather()
