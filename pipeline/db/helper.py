from db.duckdbcon import duckQueryJson, duckQueryDF
from datetime import datetime, timedelta

def get_max_retrain_date() -> str:

    query = """
    SELECT 
        MAX(date) as Max_date 
    FROM main.retrain_data
    WHERE time != 0 ;
    """
    
    df = duckQueryDF(query)
    max_date = df['Max_date'][0]
    
    return max_date

def get_min_retrain_date() -> str:

    query = """
    SELECT 
        MIN(date) as Max_date 
    FROM main.retrain_data;
    """
    
    df = duckQueryDF(query)
    min_date = df['Max_date'][0]
    
    return min_date

def get_today():
    return datetime.today().strftime("%Y-%m-%d")

def get_today_minus_1():
    return (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

def get_today_minus_3():
    return (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d")

def get_date_minus(date_str: str, num_days: int):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt - timedelta(days=num_days)).strftime("%Y-%m-%d")

def get_date_plus(date_str: str, num_days: int):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt + timedelta(days=num_days)).strftime("%Y-%m-%d")

def get_today_plus_num(num_days: int):
    return (datetime.today() + timedelta(days=num_days)).strftime("%Y-%m-%d")