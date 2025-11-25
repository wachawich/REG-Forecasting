from functions.merge_df import  forecast_feature_data

def fetch_weather_data():
    
    df = forecast_feature_data()
    df.to_parquet("/opt/airflow/shared/tmp_weather.parquet")
    

fetch_weather_data()