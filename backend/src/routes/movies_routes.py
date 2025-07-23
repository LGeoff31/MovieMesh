from fastapi import APIRouter, Depends
from typing import List
from database import get_db
from models.models import MovieOut, RatingByUserOut
from services.movies_services import (
    search_movies, 
    get_movie_detail, 
    get_random_movie, 
    search_autocomplete, 
    get_top_movies, 
    get_rating_chart, 
    get_rating_by_user
)
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/search", response_model=List[MovieOut])
def search(q: str, db=Depends(get_db)):
    """Search for movies by title"""
    return search_movies(db, q)

@router.get("/autocomplete", response_model=List[MovieOut])
def autocomplete(q: str, db=Depends(get_db)):
    """Autocomplete for movie titles"""
    return search_autocomplete(db, q)

_random_cache = {"movies": None, "last_updated": None} # cache for random movie

@router.get("/random", response_model=List[MovieOut])
def random_movie(db=Depends(get_db)):
    """Get random movie, cached daily"""
    now = datetime.now()
    if not _random_cache["movies"] or not _random_cache["last_updated"] or now - _random_cache["last_updated"] > timedelta(days=1):
        _random_cache["movies"] = get_random_movie(db)
        _random_cache["last_updated"] = now
        
    return _random_cache["movies"]

@router.get("/top", response_model=List[MovieOut])
def top_movies(db=Depends(get_db)):
    """Get top movies by average rating across all reviews"""
    return get_top_movies(db)

@router.get("/{movie_id}/rating_chart", response_model=List[int])
def rating_chart(movie_id: int, db=Depends(get_db)):
    """Get rating chart for a specific movie"""
    return get_rating_chart(db, movie_id)

@router.get("/{movie_id}/rating_by_user/{user_id}", response_model=float|None)
def rating_by_user(movie_id: int, user_id: int, db=Depends(get_db)):
    """Get rating by user"""
    res = get_rating_by_user(db, movie_id, user_id)
    return res

@router.get("/{movie_id}")
def movie_detail(movie_id: int, db=Depends(get_db)):
    """Get detailed information about a specific movie"""
    return get_movie_detail(db, movie_id)