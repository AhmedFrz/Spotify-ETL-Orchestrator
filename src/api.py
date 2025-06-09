# uvicorn api:app --host 0.0.0.0 --port 8080
# http://127.0.0.1:8080/songs

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend
from typing import Optional, List
import duckdb
import os
from pydantic import BaseModel
from contextlib import contextmanager

# ---------------------- App Setup ----------------------
app = FastAPI(title="Songs API", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

# ---------------------- Database ----------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage.db")

@contextmanager
def get_db():
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        yield con
    finally:
        con.close()

# ---------------------- Models ----------------------
class Song(BaseModel):
    title: str
    artist: str
    text: Optional[str] = None
    Genre: Optional[str] = None
    Album: Optional[str] = None
    emotion: Optional[str] = None
    Popularity: Optional[int] = None
    Energy: Optional[int] = None
    Danceability: Optional[int] = None

# ---------------------- Endpoints ----------------------
@app.get("/songs", response_model=List[Song])
@cache(expire=300)
async def get_songs(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    with get_db() as con:
        return con.execute("SELECT * FROM songs LIMIT ? OFFSET ?", [limit, offset]).df().to_dict("records")

@app.get("/songs/search", response_model=List[Song])
@cache(expire=300)
async def search_songs(q: str = Query(..., min_length=1)):
    with get_db() as con:
        query = "SELECT * FROM songs WHERE title ILIKE ? OR artist ILIKE ? LIMIT 50"
        return con.execute(query, [f"%{q}%", f"%{q}%"]).df().to_dict("records")

@app.get("/analytics/top-artists")
@cache(expire=600)
async def top_artists(limit: int = Query(10, ge=1, le=50)):
    with get_db() as con:
        return con.execute("""
            SELECT artist, COUNT(*) as song_count 
            FROM songs 
            GROUP BY artist 
            ORDER BY song_count DESC 
            LIMIT ?
        """, [limit]).df().to_dict("records")

@app.get("/analytics/stats")
@cache(expire=600)
async def get_stats():
    with get_db() as con:
        return con.execute("""
            SELECT 
                COUNT(*) as total_songs,
                COUNT(DISTINCT artist) as unique_artists,
                COUNT(DISTINCT Genre) as genres,
                AVG(Popularity) as avg_popularity,
                AVG(Energy) as avg_energy,
                AVG(Danceability) as avg_danceability
            FROM songs
        """).df().to_dict("records")[0]

@app.get("/analytics/emotions")
@cache(expire=600)
async def emotion_distribution():
    with get_db() as con:
        return con.execute("""
            SELECT emotion, COUNT(*) as count 
            FROM songs 
            WHERE emotion IS NOT NULL 
            GROUP BY emotion 
            ORDER BY count DESC
        """).df().to_dict("records")

@app.get("/health")
async def health():
    try:
        with get_db() as con:
            con.execute("SELECT 1").fetchone()
        return {"status": "healthy"}
    except:
        raise HTTPException(status_code=503, detail="Database unavailable")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)