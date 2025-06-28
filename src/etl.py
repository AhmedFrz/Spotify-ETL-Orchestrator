# ETL pipeline: Ingest, transform, and store data using Polars, Pandas, and DuckDB

import polars as pl
import pandas as pd
import duckdb
import kagglehub
import os
from utils.duckdb_util import get_duckdb_connection, create_table_from_df
from utils.polars_util import read_csv_with_polars

# Download latest version of the dataset from KaggleHub
kaggle_path = kagglehub.dataset_download("devdope/900k-spotify")
print("Path to dataset files:", kaggle_path)

# Find the CSV file in the downloaded dataset directory
def find_csv_file(directory):
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            return os.path.join(directory, file)
    return None

csv_path = find_csv_file(kaggle_path)
if not csv_path:
    raise FileNotFoundError("No CSV file found in the Kaggle dataset directory.")

# Set DuckDB path to always be inside the project directory
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "storage.db")

def main():
    # 1. Read CSV with Polars
    pl_df = read_csv_with_polars(csv_path)
    print("Polars DataFrame loaded:")
    print(pl_df.head())
    print("Total records (Polars):", pl_df.shape[0])

    # 2. Convert to Pandas
    pd_df = pl_df.to_pandas()
    print("Converted to Pandas DataFrame:")
    print(pd_df.head())
    print("Total records (Pandas):", pd_df.shape[0])

    # 3. Store in DuckDB
    con = get_duckdb_connection(db_path)
    create_table_from_df(con, pd_df, table_name="songs")
    result = con.execute("SELECT COUNT(*) FROM songs").fetchone()
    print("Total records in DuckDB table 'songs':", result[0])
    print("Data loaded into DuckDB table 'songs'.")

if __name__ == "__main__":
    main()
