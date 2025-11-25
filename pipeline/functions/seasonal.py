from tqdm import tqdm
import pandas as pd
import numpy as np

from astral.sun import sun
from pysolar.solar import get_altitude
from datetime import datetime

from functions.variable import LAT, LON, START_DATE, END_DATE, CITY, TZINFO, SEASON_VARS


def get_season(d):
    m = d.month
    day = d.day
    if (m == 12 and day >= 21) or (m <= 3 and (m < 3 or (m == 3 and day <= 19))):
        return "Winter"
    elif (m == 3 and day >= 20) or (m < 6) or (m == 6 and day <= 20):
        return "Spring"
    elif (m == 6 and day >= 21) or (m < 9) or (m == 9 and day <= 21):
        return "Summer"
    else:
        return "Autumn"
    

def process_seasonal_data(start_date = START_DATE, end_date = END_DATE):
    
    period = pd.date_range(start=f"{start_date}", end=f"{end_date}", freq='h')
    season_df = pd.DataFrame({'period': period})

    season_df["date"] = season_df["period"].dt.normalize()

    season_df['day_of_year'] = season_df['date'].dt.dayofyear
    season_df['month'] = season_df['date'].dt.month

    season_df['sin_doy'] = np.sin(2 * np.pi * season_df['day_of_year'] / 365)
    season_df['cos_doy'] = np.cos(2 * np.pi * season_df['day_of_year'] / 365)

    season_df['season'] = season_df['date'].apply(get_season)

    season_df["time"] = season_df["period"].dt.strftime("%H:%M")
    
    sunrise_list, sunset_list, zenith_list = [], [], []

    for ts in tqdm(season_df['date']):
        s = sun(CITY.observer, date=ts.date(), tzinfo=TZINFO)
        sunrise_list.append(s['sunrise'].isoformat())
        sunset_list.append(s['sunset'].isoformat())

        local_noon = datetime(ts.year, ts.month, ts.day, 12, 0, 0, tzinfo=TZINFO)
        zenith_angle = 90 - get_altitude(LAT, LON, local_noon)
        zenith_list.append(zenith_angle)

    season_df['sunrise'] = sunrise_list
    season_df['sunset'] = sunset_list
    season_df['solar_zenith_noon_deg'] = zenith_list
    
    season_df['sunrise_time'] = season_df['sunrise'].apply(lambda x: x.split("T")[1].split(".")[0])
    season_df['sunset_time'] = season_df['sunset'].apply(lambda x: x.split("T")[1].split(".")[0])

    season_df['sunrise_time_h'] = season_df['sunrise'].apply(lambda x: int(x.split("T")[1].split(":")[0]))
    season_df['sunrise_time_m'] = season_df['sunrise'].apply(lambda x: int(x.split("T")[1].split(":")[1]))

    season_df['sunset_time_h'] = season_df['sunset'].apply(lambda x: int(x.split("T")[1].split(":")[0]))
    season_df['sunset_time_m'] = season_df['sunset'].apply(lambda x: int(x.split("T")[1].split(":")[1]))

    season_df['date'] = season_df['date'].dt.normalize()

    season_df["season"] = season_df["season"].map({
        "Winter": 1,
        "Spring": 2,
        "Summer": 3,
        "Autumn": 4
    })

    return season_df

def pre_process_seasonal_day(season_df):
    
    season_df["year"] = season_df["period"].dt.year
    season_df["month"] = season_df["period"].dt.month
    season_df["day"] = season_df["period"].dt.day
    
    return season_df

def seasonal_df(start_date=START_DATE, end_date=END_DATE):
    
    df = process_seasonal_data(start_date, end_date)
    season_data = df[SEASON_VARS]
    
    return season_data

def seasonal_day_df(start_date=START_DATE, end_date=END_DATE):
    
    df = process_seasonal_data(start_date, end_date)
    clean_df = pre_process_seasonal_day(df)
    season_data = clean_df[SEASON_VARS + ['year', 'month', 'day']]
    
    return season_data


