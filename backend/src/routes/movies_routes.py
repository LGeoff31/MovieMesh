from fastapi import APIRouter, Depends
from typing import List
from database import get_db
from models.models import MovieOut
from services.movies_services import search_movies, get_movie_detail, get_random_movie, search_autocomplete
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

@router.get("/{movie_id}")
def movie_detail(movie_id: int, db=Depends(get_db)):
    """Get detailed information about a specific movie"""
    return get_movie_detail(db, movie_id)