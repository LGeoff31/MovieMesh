from fastapi import APIRouter, Depends
from typing import List
from database import get_db
from models.models import MovieOut
from services.movies_services import search_movies, get_movie_detail

router = APIRouter()


@router.get("/search", response_model=List[MovieOut])
def search(q: str, db=Depends(get_db)):
    """Search for movies by title"""
    return search_movies(db, q)


@router.get("/{movie_id}")
def movie_detail(movie_id: int, db=Depends(get_db)):
    """Get detailed information about a specific movie"""
    return get_movie_detail(db, movie_id)
