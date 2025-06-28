# Data profiling utilities using YData Profiling

import pandas as pd
from ydata_profiling import ProfileReport
from utils.duckdb_util import get_duckdb_connection
import os

def generate_profile_report(table_name: str = "songs", db_path: str = None, output_html: str = "profile_report.html"):
    # Always use storage.db in the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if db_path is None:
        db_path = os.path.join(script_dir, "storage.db")

    # Connect to DuckDB and load data into pandas DataFrame
    con = get_duckdb_connection(db_path)

    # Limit to first 1000 rows for profiling
    df = con.execute(f"SELECT * FROM {table_name} LIMIT 1000").df()
    print(f"Loaded {len(df)} records from table '{table_name}' for profiling.")

    # Generate profile report
    # Save the report in the same directory as this script
    output_path = os.path.join(script_dir, output_html)
    profile = ProfileReport(df, title=f"Profiling Report for {table_name} (first 1000 rows)", explorative=True)
    profile.to_file(output_path)
    print(f"Profile report saved to {output_path}.")

if __name__ == "__main__":
    generate_profile_report()
