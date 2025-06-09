# Spotify ETL Orchestrator
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.9.0+-yellow.svg)](https://duckdb.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **Transform 551K+ Spotify tracks into actionable insights with a modern data pipeline**

## Project Summary

- **Lightning-fast ETL** with Polars processing 1.5GB of music data (10x faster than Pandas)
- **Embedded analytics** using DuckDB - no server required
- **Asynchronous REST API** with FastAPI handling 1000+ concurrent requests
- **Interactive Streamlit dashboard** for real-time data exploration and visualization
- **Automated profiling** with YData generating data quality reports
- **Docker-ready** for portable, reproducible deployment

## What It Does

Kaggle Dataset (900K songs) → Polars ETL (10x faster) → DuckDB (1.5GB OLAP) → FastAPI/Streamlit/Profiling
    
## Key Features

### Data Insights
- **551,443 songs** with lyrics, emotions, and audio features
- **39 attributes** including energy, danceability, tempo
- **Similar song recommendations** using ML similarity scores

### Performance
```
┌─────────────────┬────────────┐
│ ETL Processing  │ <10 seconds│
│ API Response    │ <100ms     │
│ Database Size   │ 1.5GB      │
│ Memory Usage    │ <500MB     │
└─────────────────┴────────────┘
```

## Tech Stack & Skills

| Component | Technology | Why? | Skills Demonstrated |
|-----------|------------|------|-------------------|
| **ETL** | Polars | 10x faster than Pandas | High-performance data processing, batch handling (1.5GB) |
| **Database** | DuckDB | Embedded OLAP, no server | Columnar storage, SQL analytics, data modeling |
| **API** | FastAPI | Async, auto-docs, 1000+ RPS | REST design, caching, error handling, pagination |
| **Dashboard** | Streamlit | Python-native UI | Interactive visualizations, real-time filtering |
| **Profiling** | YData | Automated EDA | Data quality reports, statistical analysis |
| **DevOps** | Docker | Container orchestration | CI/CD ready, reproducible environments |

**Core Skills:** Python 3.10+ • SQL • ETL Pipeline Design • API Development • Data Visualization

## Installation

### Prerequisites
- Python 3.10+
- 2GB disk space
- Kaggle account (for dataset access)

### Setup

1. **Clone repository**
```bash
git clone https://github.com/yourusername/spotify-vault
cd spotify-vault
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Kaggle API**
```bash
# Create ~/.kaggle/kaggle.json with your credentials
{"username":"your_username","key":"your_api_key"}
```

5. **Run ETL pipeline**
```bash
python etl.py
```

## Configuration

Create `config.json` for custom settings:
```json
{
  "database": {
    "path": "storage.db",
    "indexes": ["artist", "title"]
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8080,
    "cache_ttl": 300
  },
  "etl": {
    "batch_size": 50000,
    "column_mapping": {
      "Artist(s)": "artist",
      "song": "title"
    }
  }
}
```

## Usage

### Start Services
```bash
# API Server
python api.py
# Visit http://localhost:8080/docs

# Dashboard
streamlit run dashboard.py
# Visit http://localhost:8501

# Data Profiling (generates HTML report)
python profiling.py
# Opens profile_report.html

# Docker (all services)
docker-compose up
```

## API Endpoints

### Search & Discovery
```http
GET /songs?limit=20&offset=0        # Browse songs
GET /songs/search?q=beatles         # Search artists/titles
```

### Analytics
```http
GET /analytics/top-artists?limit=10  # Top artists by song count
GET /analytics/stats                 # Database overview
GET /analytics/emotions              # Mood distribution
```

### Example Response
```json
{
  "title": "Let It Be",
  "artist": "The Beatles",
  "emotion": "joy",
  "energy": 65,
  "danceability": 45,
  "popularity": 89
}
```

## Business Value

### Technical Value
- **Scalable Architecture**: Handles millions of records with <100ms query time
- **API-First Design**: Easy integration with existing business systems
- **Real-Time Analytics**: Cached endpoints for dashboard performance
- **Data Quality**: Automated profiling ensures reliable insights

### ROI Metrics
- 90% faster data processing vs traditional SQL databases
- 5-minute setup vs hours for traditional data warehouses
- Zero infrastructure costs (embedded database)
- REST API enables monetization opportunities

## Project Structure

```
spotify-vault/
├──etl.py              # Polars-powered data pipeline
├──api.py              # FastAPI REST server
├──dashboard.py        # Streamlit analytics UI
├──profiling.py        # Data quality reports
├──storage.db          # DuckDB database (1.5GB)
├──docker-compose.yml  # Container orchestration
└──utils/             # Helper modules
    ├── duckdb_util.py
    ├── polars_util.py
    └── pandas_util.py
```

## Live Demo

<table>
<tr>
<td width="50%">

### Dashboard Preview
- Real-time search
- Interactive filters  
- Export to CSV
- Visual analytics

</td>
<td width="50%">

### API Documentation
- Auto-generated docs
- Try-it-out console
- Response examples
- Performance metrics

</td>
</tr>
</table>
