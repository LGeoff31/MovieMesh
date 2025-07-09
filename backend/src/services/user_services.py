from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy import text
from fastapi import HTTPException, status
from utils.sql_utils import load_sql
from models.models import UserCreate, UserInDB, TokenData
import jwt
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_username(db, username: str) -> Optional[UserInDB]:
    """Get user by username from database"""
    sql = text(load_sql("users/get_user.sql"))
    result = db.execute(sql, {"username": username}).mappings().first()
    
    if result:
        return UserInDB(**result)
    return None


def authenticate_user(db, username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_user(db, user: UserCreate) -> UserInDB:
    """Create a new user with hashed password"""
    # Check if username already exists
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Insert user into database
    sql = text(load_sql("users/create_user.sql"))
    result = db.execute(sql, {
        "username": user.username,
        "name": user.name,
        "password_hash": hashed_password
    })
    db.commit()
    
    # Get the created user
    user_id = result.lastrowid
    return UserInDB(
        user_id=user_id,
        username=user.username,
        name=user.name,
        password_hash=hashed_password
    )


def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError):
        return None


def get_current_user(db, token: str) -> UserInDB:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    
    return user 