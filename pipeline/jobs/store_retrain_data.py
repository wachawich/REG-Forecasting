import pandas as pd
from db.duckdbcon import get_duckdb_connection
from functions.merge_df import date_post_process

df = pd.read_parquet("/opt/airflow/shared/tmp_retrain_weather.parquet")

con = get_duckdb_connection()

# # Insert data
con.execute("""
    INSERT INTO retrain_data
    SELECT * FROM df
""")

print("Data loaded retrain data into DuckDB successfully.")
