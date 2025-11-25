import pandas as pd
import numpy as np

from functions.weather import weather_df, weather_forecast_df
from functions.seasonal import seasonal_df, seasonal_day_df
from functions.electic import electic_df

from db.helper import get_max_retrain_date, get_min_retrain_date, get_today, get_today_minus_1, get_today_minus_3, get_today_plus_num
from functions.variable import FORECAST_RANGE_DAYS, SOLAR, WIND

def merge_historical_data(start_date, end_date):
    weather_data = weather_df(start_date, end_date)
    seasonal_data = seasonal_df(start_date, end_date)
    electic_data = electic_df(start_date, end_date)

    merged_df = weather_data.merge(
        seasonal_data,
        on=["date", "time"],
        how="left"
    )

    merged_df = merged_df.merge(
        electic_data,
        on=["date", "time"],
        how="left"
    )

    return merged_df

def merge_forecast_data():
    
    start_date_minus_3 = get_today_minus_3()
    end_date_minus_1 = get_today_minus_1()
    end_date_plus_num = get_today_plus_num(FORECAST_RANGE_DAYS)
    
    print(f"Forecast merge range: {start_date_minus_3} to {end_date_plus_num}")
    
    weather_data = weather_df(start_date_minus_3, end_date_minus_1)
    weather_forecast_data = weather_forecast_df()
    seasonal_data = seasonal_day_df(start_date_minus_3, end_date_plus_num)
    
    merged_weather = pd.concat(
        [weather_data, weather_forecast_data],
        ignore_index=True
    )

    final_df = merged_weather.merge(
        seasonal_data,
        on=["date", "time"],
        how="left"
    )

    return final_df

def final_elec_post_process(merged_df):
    merged_df["time"] = merged_df["time"].str.slice(0, 2).astype(int)

    merged_df["sin_time"] = np.sin(2 * np.pi * merged_df["time"] / 24)
    merged_df["cos_time"] = np.cos(2 * np.pi * merged_df["time"] / 24)

    merged_df["day_of_month_sin"] = np.sin(2 * np.pi * merged_df["day"] / 31)
    merged_df["day_of_month_cos"] = np.cos(2 * np.pi * merged_df["day"] / 31)

    merged_df["month_of_year_sin"] = np.sin(2 * np.pi * merged_df["month"] / 12)
    merged_df["month_of_year_cos"] = np.cos(2 * np.pi * merged_df["month"] / 12)
    
    merged_df['date'] = merged_df['date'].astype(str)
    df_cleaned = merged_df.dropna(subset=['value'])
    df_cleaned.loc[:, 'value'] = df_cleaned['value'].astype(int)
    
    return df_cleaned

def date_post_process(merged_df):
    merged_df['date'] = merged_df['date'].astype(str)
    return merged_df

def final_non_elec_post_process(merged_df):
    merged_df["time"] = merged_df["time"].str.slice(0, 2).astype(int)

    merged_df["sin_time"] = np.sin(2 * np.pi * merged_df["time"] / 24)
    merged_df["cos_time"] = np.cos(2 * np.pi * merged_df["time"] / 24)

    merged_df["day_of_month_sin"] = np.sin(2 * np.pi * merged_df["day"] / 31)
    merged_df["day_of_month_cos"] = np.cos(2 * np.pi * merged_df["day"] / 31)

    merged_df["month_of_year_sin"] = np.sin(2 * np.pi * merged_df["month"] / 12)
    merged_df["month_of_year_cos"] = np.cos(2 * np.pi * merged_df["month"] / 12)
    
    merged_df["solar_count"] = merged_df["year"].map(SOLAR)
    merged_df["wind_turbine_count"] = merged_df["year"].map(WIND)
    
    merged_df['date'] = merged_df['date'].astype(str)
    
    return merged_df


def historical_feature_data(start_date, end_date):
    
    merged_df = merge_historical_data(start_date, end_date)
    final_df = final_elec_post_process(merged_df)
    
    return final_df

def retrain_feature_data(start_date, end_date):
    
    merged_df = merge_historical_data(start_date, end_date)
    final_df = final_elec_post_process(merged_df)
    
    return final_df

def forecast_feature_data():
    
    merged_df = merge_forecast_data()
    final_df = final_non_elec_post_process(merged_df)
    
    return final_df