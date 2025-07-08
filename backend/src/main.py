from fastapi import FastAPI, Depends, HTTPException, status, Cookie, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from typing import List
from database import get_db, fetch_all
from utils.sql_utils import load_sql
from models.models import MovieOut, ReviewIn, ReviewOut
from routes.reviews_routes import router as reviews_router


app = FastAPI(title="IMDB-Clone API", docs_url="/api/docs", openapi_url="/api/openapi.json")
# app.include_router(reviews_router, prefix="/api") // TODO: fix

# allow front-end JS served by same host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ─────────────────────────── ROUTES ────────────────────────────
@app.get("/api/search", response_model=List[MovieOut])
def search(q: str, db=Depends(get_db)):
    sql = text(load_sql("utils/search_movies.sql"))
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

@app.post("/api/login")
def login(data: dict, response: Response):
    # Replace with real authentication logic
    if data["username"] == "user" and data["password"] == "pass":
        # Set a secure, HTTP-only cookie
        response.set_cookie(
            key="session", 
            value="some-session-token", 
            httponly=True, 
            secure=True, 
            samesite="lax"
        )
        return {"message": "Logged in"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out"}

@app.get("/api/check-auth")
def check_auth(session: str = Cookie(None)):
    if session == "some-session-token":
        return {"logged_in": True}
    return JSONResponse({"logged_in": False}, status_code=401)


# ───────────────────────── STATIC FRONTEND ─────────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
