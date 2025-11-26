from functions.merge_df import retrain_feature_data
from db.helper import get_max_retrain_date, get_today_minus_1, get_date_minus, get_date_plus

def fetch_retrain_data():
    
    start_date = get_max_retrain_date()
    real_start_date = get_date_plus(start_date, 1)
    
    print(start_date, real_start_date)
    start_date_minus = get_date_minus(start_date, 3)
    end_date = get_today_minus_1()
    
    # if start_date == end_date:
    #     print("No new data, skip")
    #     raise AirflowSkipException("No new data")
    
    df_re_predict = retrain_feature_data(start_date_minus, end_date)
    df_re_predict = df_re_predict[df_re_predict['date'] != end_date]
    df_re_predict.to_parquet("/opt/airflow/shared/tmp_repredict_weather.parquet")
    
    df = retrain_feature_data(real_start_date, end_date)
    df = df[df['date'] != end_date]
    df.to_parquet("/opt/airflow/shared/tmp_retrain_weather.parquet")
    
    # print(f"Retrain data fetch range: {start_date} to {end_date}")
    

fetch_retrain_data()