from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from database import get_db
from services.user_services import get_current_user
from services.reviews_services import get_reviews_by_user
from models.models import ReviewOut, UserOut, ReviewOutWithMovie

router = APIRouter()
security = HTTPBearer(auto_error=False)

@router.get("/me", response_model=UserOut)
def me(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = get_current_user(db, credentials.credentials)
    return UserOut(user_id=user.user_id, username=user.username, name=user.name)

@router.get("/me/reviews", response_model=List[ReviewOutWithMovie])
def my_reviews(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = get_current_user(db, credentials.credentials)
    return get_reviews_by_user(user.user_id, db) 