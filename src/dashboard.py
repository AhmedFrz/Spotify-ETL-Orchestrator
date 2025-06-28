# to run the file - streamlit run dashboard.py

import streamlit as st
import duckdb
import pandas as pd
import os

st.title("Unified Data Engineering Dashboard")

# User control for number of rows to preview
row_count = st.sidebar.slider("Rows to preview", 1, 100, 10)

def get_db_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "storage.db")

def load_data(table_name: str = "songs", limit: int = 10):
    con = duckdb.connect(get_db_path())
    df = con.execute(f"SELECT * FROM {table_name} LIMIT {limit}").df()
    con.close()
    return df.astype(str)  # Ensure all columns are string for Streamlit compatibility

# Load data
data = load_data(limit=row_count)

# Column selector
columns = st.multiselect("Select columns to display", data.columns.tolist(), default=data.columns.tolist())

# Search/filter
search = st.text_input("Search (case-insensitive, any column)")
if search and columns:
    mask = data[columns].apply(lambda col: col.str.contains(search, case=False, na=False))
    filtered = data[mask.any(axis=1)]
else:
    filtered = data

# Data preview
st.subheader("Sample Data from DuckDB")
st.dataframe(filtered[columns] if columns else filtered)

# Download button
st.download_button("Download CSV", filtered[columns].to_csv(index=False) if columns else filtered.to_csv(index=False), "songs_preview.csv")

# Summary statistics
if columns:
    st.subheader("Summary Statistics")
    st.write(filtered[columns].describe())

# Simple bar chart (if at least 2 columns)
if columns and len(columns) >= 2:
    st.subheader("Bar Chart")
    x_col = st.selectbox("X axis", columns, index=0)
    y_col = st.selectbox("Y axis", columns, index=1)
    st.bar_chart(filtered[[x_col, y_col]])

