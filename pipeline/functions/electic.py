import requests
import pandas as pd

from dateutil.relativedelta import relativedelta

from functions.variable import SOLAR, WIND, START_DATE, END_DATE, ELECTIC_API_KEY, RENEWABLE, RESPONDENTS, ELECTRICITY_VARS, ELECTRICITY_API_URL


def fetch_eia_data(start_date=START_DATE, end_date=END_DATE, api_key=ELECTIC_API_KEY, respondents=RESPONDENTS, fueltypes=RENEWABLE):
    
    dfs = []
    current_start = pd.to_datetime(start_date)
    final_end = pd.to_datetime(end_date)

    while current_start <= final_end:
        current_end = min(current_start + relativedelta(months=3) - pd.Timedelta(days=1), final_end)
        
        elec_url = (
            f"{ELECTRICITY_API_URL}"
            f"?api_key={api_key}"
            "&frequency=hourly"
            "&data[0]=value"
        )
        
        for r in respondents:
            elec_url += f"&facets[respondent][]={r}"
        for f in fueltypes:
            elec_url += f"&facets[fueltype][]={f}"
        
        elec_url += f"&start={current_start.strftime('%Y-%m-%dT%H')}"
        elec_url += f"&end={current_end.strftime('%Y-%m-%dT%H')}"
        
        resp = requests.get(elec_url)
        resp.raise_for_status()
        data = resp.json()
        
        if "response" in data and "data" in data["response"]:
            df = pd.DataFrame(data["response"]["data"])
            dfs.append(df)
        
        current_start = current_end + pd.Timedelta(hours=1)

    full_df = pd.concat(dfs, ignore_index=True)
    
    return full_df


def electic_data_preprocess(elec_res_df, solar=SOLAR, wind=WIND):
    
    elec_res_df["period"] = pd.to_datetime(elec_res_df["period"])
    elec_res_df["date"] = elec_res_df["period"].dt.normalize()

    elec_res_df["year"] = elec_res_df["period"].dt.year
    elec_res_df["month"] = elec_res_df["period"].dt.month
    elec_res_df["day"] = elec_res_df["period"].dt.day

    elec_res_df["time"] = elec_res_df["period"].dt.strftime("%H:%M")
    
    elec_renewable = elec_res_df[elec_res_df["fueltype"].isin(RENEWABLE)]
    elec_renewable["fueltype"] = elec_renewable["fueltype"].map({
        "SUN": 1,
        "WND": 2
    })
    
    elec_renewable["solar_count"] = elec_renewable["year"].map(solar)
    elec_renewable["wind_turbine_count"] = elec_renewable["year"].map(wind)
    
    elec_renewable = elec_renewable.dropna()
    
    return elec_renewable

def electic_df(start_date=START_DATE, end_date=END_DATE):
    
    elec_res_df = fetch_eia_data(start_date, end_date)
    clean_df = electic_data_preprocess(elec_res_df)
    electic_data = clean_df[ELECTRICITY_VARS]
    
    return electic_data