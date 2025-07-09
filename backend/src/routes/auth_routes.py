from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from database import get_db
from services.auth_services import login_user, logout_user, check_authentication
from services.user_services import create_user, get_current_user
from models.models import UserCreate, UserLogin, UserOut, Token

router = APIRouter()
security = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db=Depends(get_db)):
    """Register a new user"""
    db_user = create_user(db, user)
    return UserOut(
        user_id=db_user.user_id,
        username=db_user.username,
        name=db_user.name
    )


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db=Depends(get_db)):
    """User login endpoint"""
    res = login_user(db, user_login)
    print(res)
    return res


@router.get("/me", response_model=UserOut)
def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    print("Getting current user information")
    """Get current user information"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_current_user(db, credentials.credentials)
    return UserOut(
        user_id=user.user_id,
        username=user.username,
        name=user.name
    )


@router.get("/check-auth")
def check_auth(
    authorization: Optional[str] = Header(None),
    db=Depends(get_db)
):
    """Check if user is authenticated"""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]  # Remove "Bearer " prefix
    
    result = check_authentication(db, token)
    if result["logged_in"]:
        return result
    return JSONResponse(result, status_code=401)
