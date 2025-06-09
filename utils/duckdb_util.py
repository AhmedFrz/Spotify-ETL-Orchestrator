# Utility functions for DuckDB operations

import os
import duckdb
import pandas as pd

def get_duckdb_connection(db_path: str = None):
    """Get or create a DuckDB connection in the project directory by default."""
    if db_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "..", "storage.db")
        db_path = os.path.abspath(db_path)
    return duckdb.connect(db_path)

# def create_table_from_df(con, df: pd.DataFrame, table_name: str):
#     """Create or replace a DuckDB table from a pandas DataFrame."""
#     con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")

def create_table_from_df(con, df: pd.DataFrame, table_name: str):
    """Create or replace a DuckDB table from a pandas DataFrame."""
    con.register('df_temp', df)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_temp")
    con.unregister('df_temp')
