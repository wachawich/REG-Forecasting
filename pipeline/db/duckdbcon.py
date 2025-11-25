import duckdb
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv("/opt/airflow/.env")

def get_duckdb_connection():
    """
    Connect to DuckDB
    """
    
    mother_duck_token = os.getenv("MOTHER_DUCK_TOKEN")
    db_name = "REG-Forecasting"
    
    con = duckdb.connect(f"md:{db_name}?motherduck_token={mother_duck_token}")
    
    return con

def duckQueryJson(query : str):
    """
    Execute a query on DuckDB and return results as JSON
    """
    con = get_duckdb_connection()
    result = con.execute(query).fetchall()
    columns = [desc[0] for desc in con.description]
    
    # Convert results to list of dictionaries
    results_list = [dict(zip(columns, row)) for row in result]
    
    return jsonify(results_list)

def duckQueryDF(query : str):
    """
    Execute a query on DuckDB and return results as JSON
    """
    con = get_duckdb_connection()
    result = con.execute(query).df()
    
    return result