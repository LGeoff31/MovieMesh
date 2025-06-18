from fastapi import APIRouter, Depends, HTTPException
from services.reviews_services import check_movie_exists, add_review, get_reviews_by_movie
from models.models import ReviewIn, ReviewOut
from database import get_db

router = APIRouter()

@router.post("/movies/{movie_id}/reviews")
def add_review(movie_id: int, review: ReviewIn, db=Depends(get_db)):
    if not check_movie_exists(movie_id, db):
        raise HTTPException(404, "Movie not found")
    add_review(movie_id, review.user_id, review.rating, review.comment, db)
    return {"message": "Review added successfully"}
    
@router.get("/movies/{movie_id}/reviews")
def get_reviews(movie_id: int, db=Depends(get_db)):
    return get_reviews_by_movie(movie_id, db)