# uvicorn api:app --host 0.0.0.0 --port 808
# http://127.0.0.1:8081/songs

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import duckdb
import os
from contextlib import contextmanager

# ---------------------- App Setup ----------------------
app = FastAPI(title="Songs API", version="2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------- Database ----------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage.db")

@contextmanager
def get_db():
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        yield con
    finally:
        con.close()

# ---------------------- Endpoints ----------------------
@app.get("/songs")
async def get_songs(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    with get_db() as con:
        # Get all columns dynamically
        columns = [row[1] for row in con.execute("PRAGMA table_info('songs')").fetchall()]
        query = f"SELECT * FROM songs LIMIT ? OFFSET ?"
        rows = con.execute(query, [limit, offset]).fetchdf()
        return rows.to_dict("records")

@app.get("/songs/search")
async def search_songs(q: str = Query(..., min_length=1)):
    with get_db() as con:
        columns = [row[1] for row in con.execute("PRAGMA table_info('songs')").fetchall()]
        # Search in all text columns
        text_cols = [col for col in columns if col.lower() in ["title", "artist", "song", "artist(s)"]]
        if not text_cols:
            return []
        like_clauses = " OR ".join([f'{col} ILIKE ?' for col in text_cols])
        params = [f"%{q}%"] * len(text_cols)
        query = f"SELECT * FROM songs WHERE {like_clauses} LIMIT 50"
        rows = con.execute(query, params).fetchdf()
        return rows.to_dict("records")

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
    uvicorn.run(app, host="0.0.0.0", port=8081)