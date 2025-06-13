from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from pydantic import BaseModel, Field
from typing import List
from .database import get_db, fetch_all
from datetime import datetime

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
    rows = fetch_all(
        db,
        text("""SELECT movie_id, title, year, imdb_rating
                FROM movies WHERE title LIKE :pat ORDER BY year DESC LIMIT 30"""),
        pat=f"%{q}%")
    return rows

@app.get("/api/movies/{movie_id}")
def movie_detail(movie_id: int, db=Depends(get_db)):
    movie = db.execute(text("SELECT * FROM movies WHERE movie_id=:id"), {"id": movie_id}).mappings().first()
    if not movie:
        raise HTTPException(404, "Movie not found")

    directors = fetch_all(db, text("""
        SELECT p.name FROM people p
        JOIN movie_directors md USING(person_id)
        WHERE md.movie_id=:id
    """), id=movie_id)

    cast = fetch_all(db, text("""
        SELECT p.name, mc.cast_order FROM people p
        JOIN movie_cast mc USING(person_id)
        WHERE mc.movie_id=:id ORDER BY mc.cast_order
    """), id=movie_id)

    genres = fetch_all(db, text("""
        SELECT g.name FROM genres g
        JOIN movie_genres mg USING(genre_id)
        WHERE mg.movie_id=:id
    """), id=movie_id)

    reviews = fetch_all(db, text("""
        SELECT AVG(rating) AS avg_rating, COUNT(*) AS num_reviews
        FROM reviews WHERE movie_id=:id
    """), id=movie_id)[0]

    return {
        "movie": movie,
        "directors": [d["name"] for d in directors],
        "cast":      [c["name"] for c in cast],
        "genres":    [g["name"] for g in genres],
        "reviews_summary": reviews
    }

@app.get("/api/movies/{movie_id}/reviews", response_model=List[ReviewOut])
def list_reviews(movie_id: int, db=Depends(get_db)):
    rows = fetch_all(db, text("""
        SELECT review_id, rating, comment_txt, created_at
        FROM reviews WHERE movie_id=:id ORDER BY created_at DESC
    """), id=movie_id)
    return rows

@app.post("/api/movies/{movie_id}/reviews", status_code=status.HTTP_201_CREATED)
def add_review(movie_id: int, rev: ReviewIn, db=Depends(get_db)):
    # ensure movie exists
    if not db.execute(text("SELECT 1 FROM movies WHERE movie_id=:id"), {"id": movie_id}).first():
        raise HTTPException(404, "Movie not found")
    res = db.execute(text("""
        INSERT INTO reviews(movie_id, rating, comment_txt) VALUES(:m,:r,:c)
    """), {"m": movie_id, "r": rev.rating, "c": rev.comment})
    db.commit()
    return JSONResponse({"review_id": res.lastrowid}, status_code=201)

# ───────────────────────── STATIC FRONTEND ─────────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
