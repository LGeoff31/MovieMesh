from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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