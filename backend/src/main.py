from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from pydantic import BaseModel, Field
from typing import List
from database import get_db, fetch_all
from datetime import datetime
from utils.sql_utils import load_sql

app = FastAPI(title="IMDB-Clone API", docs_url="/api/docs", openapi_url="/api/openapi.json")

# allow front-end JS served by same host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ─────────────────────────── MODELS ────────────────────────────
class MovieOut(BaseModel):
    movie_id: int
    title: str
    year: int | None
    imdb_rating: float | None
    certificate: str | None
    runtime_min: int | None
    poster_link: str | None

class ReviewIn(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    comment: str = Field(..., max_length=1000)

class ReviewOut(BaseModel):
    review_id: int
    rating: int
    comment_txt: str
    created_at: datetime

# ─────────────────────────── ROUTES ────────────────────────────
@app.get("/api/search", response_model=List[MovieOut])
def search(q: str, db=Depends(get_db)):
    sql = text(load_sql("search_movies.sql"))
    rows = fetch_all(db, sql, pat=f"%{q}%")
    return rows

@app.get("/api/movies/{movie_id}")
def movie_detail(movie_id: int, db=Depends(get_db)):
    movie_sql = text(load_sql("detail/get_movie.sql"))
    movie = db.execute(movie_sql, {"id": movie_id}).mappings().first()

    if not movie:
        raise HTTPException(404, "Movie not found")

    directors_sql = text(load_sql("detail/get_directors.sql"))
    directors_rows = fetch_all(db, directors_sql, id=movie_id)

    cast_sql = text(load_sql("detail/get_cast.sql"))
    cast_rows = fetch_all(db, cast_sql, id=movie_id)

    genres_sql = text(load_sql("detail/get_genres.sql"))
    genres_rows = fetch_all(db, genres_sql, id=movie_id)

    summary_sql = text(load_sql("detail/get_reviews_summary.sql"))
    reviews_summary = db.execute(summary_sql, {"id": movie_id}).mappings().first()

    return {
        "movie": movie,
        "directors": [d["name"] for d in directors_rows],
        "cast":      [c["name"] for c in cast_rows],
        "genres":    [g["name"] for g in genres_rows],
        "reviews_summary": reviews_summary
    }

@app.get("/api/movies/{movie_id}/reviews", response_model=List[ReviewOut])
def list_reviews(movie_id: int, db=Depends(get_db)):
    reviews_sql = text(load_sql("reviews/get_reviews_by_movie.sql"))
    rows = fetch_all(db, reviews_sql, id=movie_id)
    return rows

@app.post("/api/movies/{movie_id}/reviews", status_code=status.HTTP_201_CREATED)
def add_review(movie_id: int, rev: ReviewIn, db=Depends(get_db)):
    # ensure movie exists
    exists_sql = text(load_sql("reviews/check_movie_exists.sql"))
    if not db.execute(exists_sql, {"id": movie_id}).first():
        raise HTTPException(404, "Movie not found")

    insert_sql = text(load_sql("reviews/add_review.sql"))
    res = db.execute(insert_sql, {"m": movie_id, "r": rev.rating, "c": rev.comment})
    db.commit()
    return JSONResponse({"review_id": res.lastrowid}, status_code=201)

# ───────────────────────── STATIC FRONTEND ─────────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
