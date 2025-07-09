from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from services.reviews_services import check_movie_exists, add_review, get_reviews_by_movie
from models.models import ReviewIn, ReviewOut
from database import get_db

router = APIRouter()

@router.post("/{movie_id}/reviews", status_code=status.HTTP_201_CREATED)
def add_review_endpoint(movie_id: int, rev: ReviewIn, db=Depends(get_db)):
    if not check_movie_exists(movie_id, db):
        raise HTTPException(404, "Movie not found")
    review_id = add_review(movie_id, rev.rating, rev.comment, rev.user_id, db)
    return JSONResponse({"review_id": review_id}, status_code=201)
    
@router.get("/{movie_id}/reviews", response_model=List[ReviewOut])
def list_reviews(movie_id: int, db=Depends(get_db)):
    return get_reviews_by_movie(movie_id, db)