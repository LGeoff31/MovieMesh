from utils.sql_utils import load_sql
from sqlalchemy import text
from database import fetch_all
from fastapi import HTTPException


def search_movies(db, search_term: str):
    """Search for movies by title"""
    sql = text(load_sql("utils/search_movies.sql"))
    rows = fetch_all(db, sql, pat=f"%{search_term}%")
    return rows


def get_movie_detail(db, movie_id: int):
    """Get detailed movie information including cast, directors, genres, and review summary"""
    # Get basic movie info
    movie_sql = text(load_sql("detail/get_movie.sql"))
    movie = db.execute(movie_sql, {"id": movie_id}).mappings().first()

    if not movie:
        raise HTTPException(404, "Movie not found")

    # Get directors
    directors_sql = text(load_sql("detail/get_directors.sql"))
    directors_rows = fetch_all(db, directors_sql, id=movie_id)

    # Get cast
    cast_sql = text(load_sql("detail/get_cast.sql"))
    cast_rows = fetch_all(db, cast_sql, id=movie_id)

    # Get genres
    genres_sql = text(load_sql("detail/get_genres.sql"))
    genres_rows = fetch_all(db, genres_sql, id=movie_id)

    # Get reviews summary
    summary_sql = text(load_sql("detail/get_reviews_summary.sql"))
    reviews_summary = db.execute(summary_sql, {"id": movie_id}).mappings().first()

    return {
        "movie": movie,
        "directors": [d["name"] for d in directors_rows],
        "cast": [c["name"] for c in cast_rows],
        "genres": [g["name"] for g in genres_rows],
        "reviews_summary": reviews_summary
    }
