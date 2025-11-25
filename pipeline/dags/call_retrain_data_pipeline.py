from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner": "airflow"}

with DAG(
    "call_retrain_data_pipeline",
    start_date=datetime(2025,11,21),
    schedule="@daily",
    catchup=False,
):

    fetch_retrain_data = BashOperator(
        task_id="fetch_retrain_data",
        bash_command="python /opt/airflow/jobs/fetch_retrain_data.py"
    )

    store_retrain_data = BashOperator(
        task_id="store_retrain_data",
        bash_command="python /opt/airflow/jobs/store_retrain_data.py"
    )
    
    re_predict_data = BashOperator(
        task_id="re_predict_data",
        bash_command="python /opt/airflow/jobs/re_predict_data.py"
    )
    
    compare_accuracy_overtime = BashOperator(
        task_id="compare_accuracy_overtime",
        bash_command="python /opt/airflow/jobs/compare_accuracy_overtime.py"
    )


    fetch_retrain_data >> store_retrain_data >> re_predict_data >> compare_accuracy_overtime
