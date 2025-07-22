from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MovieOut(BaseModel):
    movie_id: int
    title: str
    year: int | None = None
    imdb_rating: float | None = None
    certificate: str | None = None
    runtime_min: int | None = None
    poster_link: str | None = None

class ReviewIn(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    comment: str = Field(..., max_length=1000)
    user_id: int

class ReviewOut(BaseModel):
    review_id: int
    rating: int
    comment_txt: str
    created_at: datetime
    username: str
    title: str | None = None
    movie_id: int | None = None

class ReviewOutWithMovie(BaseModel):
    review_id: int
    rating: int
    comment_txt: str
    created_at: datetime
    username: str
    title: str
    movie_id: int

# User Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    user_id: int
    username: str
    name: str

class UserInDB(BaseModel):
    user_id: int
    username: str
    name: str
    password_hash: str

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ActorOut(BaseModel):
    actor_id: int
    name: str
    total_gross: float | None = None

class DirectorOut(BaseModel):
    director_id: int
    name: str
    avg_rating: float | None = None
    film_count: int | None = None