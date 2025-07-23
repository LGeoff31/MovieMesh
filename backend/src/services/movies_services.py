from utils.sql_utils import load_sql
from sqlalchemy import text
from database import fetch_all
from fastapi import HTTPException
import re

def search_movies(db, search_term: str):
    """Search for movies by title"""
    sql = text(load_sql("utils/search_movies.sql"))
    rows = fetch_all(db, sql, pat=f"%{search_term}%")
    return rows

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by",
    "for", "if", "in", "into", "is", "it", "no", "not",
    "of", "on", "or", "such", "that", "the", "their", "then",
    "there", "these", "they", "this", "to", "was", "will", "with",
}

def build_boolean_prefix(term: str) -> str | None:
    # keep only alphanumerics, lower-cased
    words = re.findall(r"[0-9a-zA-Z']+", term.lower())
    filtered = [w for w in words if len(w) >= 4 and w not in STOPWORDS]

    if not filtered:          # nothing left → don't run MATCH
        return None

    # each word: required (+) and prefix-match (*)
    return " ".join(f"+{w}*" for w in filtered)

def search_autocomplete(db, search_term: str):
    """Search for movies by title"""
    # Return empty list immediately for blank queries
    if not search_term.strip():
        return []
    
    prefix = build_boolean_prefix(search_term)
    if not prefix:
        return []

    sql = text(load_sql("utils/autocomplete.sql"))
    rows = fetch_all(db, sql, prefix=prefix)
    return rows

def get_random_movie(db):
    """Get random movie"""
    sql = text(load_sql("detail/get_random_movie.sql"))
    rows = fetch_all(db, sql)
    
    if not rows:
        raise HTTPException(404, "No movies found")
    
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

def get_rating_chart(db, movie_id: int):
    """Get rating chart for a specific movie"""
    sql = text(load_sql("reviews/count_reviews_by_rating.sql"))
    rows = db.execute(sql, {"id": movie_id}).mappings().all()
    ratings = [0] * 10
    for row in rows:
        ratings[int(row["rating"]) - 1] = row["num_reviews"]
    return ratings

def get_rating_by_user(db, movie_id: int, user_id: int):
    """Get rating by user"""
    sql = text(load_sql("reviews/rating_by_user.sql"))
    row = db.execute(sql, {"movie_id": movie_id, "user_id": user_id}).mappings().first()
    if row:
        return float(row["avg_rating"])
    return None

def get_top_movies(db):
    """Get top movies by average rating across all reviews"""
    sql = text(load_sql("lists/get_highest_rated_movies.sql"))
    rows = fetch_all(db, sql)
    return rows