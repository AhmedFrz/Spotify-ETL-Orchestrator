# to run the file
# streamlit run dashboard.py

import streamlit as st
import duckdb
import pandas as pd
import os

st.title("Unified Data Engineering Dashboard")

# User control for number of rows to preview
row_count = st.sidebar.slider("Rows to preview", 1, 100, 10)

# Column selector
columns = None

def get_db_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "storage.db")

# Connect to DuckDB and load data
def load_data(table_name: str = "songs", limit: int = 10):
    con = duckdb.connect(get_db_path())
    df = con.execute(f"SELECT * FROM {table_name} LIMIT {limit}").df()
    return df

data = load_data(limit=row_count)

# Column selector
columns = st.multiselect("Select columns to display", data.columns.tolist(), default=data.columns.tolist())

# Search/filter
search = st.text_input("Search song title (case-insensitive)")
if search:
    filtered = data[data[columns[0]].astype(str).str.contains(search, case=False, na=False)] if columns else data[data.columns[0]].astype(str).str.contains(search, case=False, na=False)
else:
    filtered = data

# Data preview
st.subheader("Sample Data from DuckDB")
st.dataframe(filtered[columns] if columns else filtered)

# Download button
st.download_button("Download CSV", filtered[columns].to_csv(index=False) if columns else filtered.to_csv(index=False), "songs_preview.csv")

# Data summary/statistics
if columns:
    st.subheader("Summary Statistics")
    st.write(filtered[columns].describe())

# Interactive chart
if columns and len(columns) >= 2:
    st.subheader("Bar Chart")
    x_col = st.selectbox("X axis", columns, index=0)
    y_col = st.selectbox("Y axis", columns, index=1)
    st.bar_chart(filtered[[x_col, y_col]])

# Profile report toggle
show_profile = st.checkbox("Show profiling report")
if show_profile and os.path.exists("profile_report.html"):
    st.subheader("Data Profiling Report (first 1000 rows)")
    with open("profile_report.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=800, scrolling=True)
elif show_profile:
    st.info("Run profiling.py to generate a profiling report.")

# Row details (expanders for each row)
st.subheader("Row Details (first 5 rows)")
for idx, row in filtered.head(5).iterrows():
    with st.expander(f"Row {idx}"):
        st.write(row)

# Sidebar filters (example: filter by year if 'year' column exists)
if 'year' in data.columns:
    min_year, max_year = int(data['year'].min()), int(data['year'].max())
    year_range = st.sidebar.slider("Filter by year", min_year, max_year, (min_year, max_year))
    filtered = filtered[(filtered['year'] >= year_range[0]) & (filtered['year'] <= year_range[1])]
    st.dataframe(filtered[columns] if columns else filtered)

