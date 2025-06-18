from pydantic import BaseModel, Field
from datetime import datetime

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