import requests
import pandas as pd
import numpy as np

from functions.variable import HOURLY_WATHER_VARS
from functions.variable import LAT, LON, TIME_ZONE_WATHER, START_DATE, END_DATE, WEATHER_API_URL, FORECAST_RANGE_DAYS


def call_wather_data(start_date = START_DATE, end_date = END_DATE):
    wather_params = {
        "latitude": LAT,
        "longitude": LON,
        "timezone": TIME_ZONE_WATHER,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(HOURLY_WATHER_VARS)
    }
    
    wather_response = requests.get(WEATHER_API_URL, params=wather_params)
    wather_data = wather_response.json()

    if "error" in wather_data:
        print("Error:", wather_data["reason"])
    else:
        wather_hourly_df = pd.DataFrame(wather_data["hourly"])
        return wather_hourly_df

def call_wather_forecast_data():
    wather_params = {
        "latitude": LAT,
        "longitude": LON,
        "timezone": TIME_ZONE_WATHER,
        "forecast_days": FORECAST_RANGE_DAYS,
        "hourly": ",".join(HOURLY_WATHER_VARS)
    }

    wather_url = "https://api.open-meteo.com/v1/forecast"
    wather_response = requests.get(wather_url, params=wather_params)
    wather_data = wather_response.json()

    if "error" in wather_data:
        print("Error:", wather_data["reason"])
    else:
        wather_hourly_forecast_df = pd.DataFrame(wather_data["hourly"])
    
    return wather_hourly_forecast_df

def preprocess_wather_df(df):
    
    df["date"] = pd.to_datetime(df["time"]).dt.normalize()
    df["time"] = pd.to_datetime(df["time"]).dt.strftime("%H:%M")
    
    return df
    

def weather_df(start_date=START_DATE, end_date=END_DATE):
    
    df = call_wather_data(start_date, end_date)
    clean_df = preprocess_wather_df(df)
    
    return clean_df

def weather_forecast_df():
    
    df = call_wather_forecast_data()
    clean_df = preprocess_wather_df(df)
    
    return clean_df