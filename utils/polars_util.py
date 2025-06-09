# Utility functions for Polars operations

import polars as pl

def read_csv_with_polars(path: str) -> pl.DataFrame:
    """Read a CSV file with Polars."""
    return pl.read_csv(path)
