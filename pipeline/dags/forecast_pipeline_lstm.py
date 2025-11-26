from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner": "airflow"}

with DAG(
    "forecast_pipeline_lstm",
    schedule="@daily",
    catchup=False,
):

    fetch_weather = BashOperator(
        task_id="fetch_weather",
        bash_command="python /opt/airflow/jobs/fetch_weather.py"
    )

    predict_weather = BashOperator(
        task_id="predict_weather",
        bash_command="python /opt/airflow/jobs/weather_predict_lstm.py"
    )

    load_to_duckdb = BashOperator(
        task_id="load_to_duckdb",
        bash_command="python /opt/airflow/jobs/load_to_duckdb.py"
    )


    fetch_weather >> predict_weather >> load_to_duckdb
