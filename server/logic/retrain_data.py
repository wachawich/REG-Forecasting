from db.duckdbcon import duckQueryJson, duckQueryDF
from flask import jsonify

def get_retrain_data(data):

    query = """
    SELECT 
        *
    FROM main.retrain_data
    """
    if 'start_date' in data and 'end_date' in data:
        query += f"""
            WHERE date BETWEEN '{data['start_date']}' AND '{data['end_date']}'
        """
    elif 'start_date' in data:
        query += f"""
            WHERE date >= '{data['start_date']}'
        """
    elif 'end_date' in data:
        query += f"""
            WHERE date <= '{data['end_date']}'
        """
    
    result = duckQueryJson(query)
    
    return result