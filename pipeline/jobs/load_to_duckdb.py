import pandas as pd
from db.duckdbcon import get_duckdb_connection

df_solar = pd.read_parquet("/opt/airflow/shared/predict_weather_forecast_solar.parquet")
df_wind = pd.read_parquet("/opt/airflow/shared/predict_weather_forecast_wind.parquet")

con = get_duckdb_connection()

# Create table
# con.execute("""
#     CREATE TABLE result_forecast_solar_value AS 
#     SELECT * FROM df_solar
# """)

# con.execute("""
#     CREATE TABLE result_forecast_wind_value AS 
#     SELECT * FROM df_wind
# """)

# # Insert data
con.execute("""
    INSERT INTO result_forecast_solar_value
    SELECT * FROM df_solar
""")

con.execute("""
    INSERT INTO result_forecast_wind_value
    SELECT * FROM df_wind
""")

print("Data loaded into DuckDB successfully.")
