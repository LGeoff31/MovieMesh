from fastapi import HTTPException, Response, status
from datetime import timedelta
from services.user_services import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models.models import UserLogin, Token


def login_user(db, user_login: UserLogin) -> Token:
    """Handle user login with JWT token"""
    user = authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


def logout_user(response: Response):
    """Handle user logout by clearing session cookie"""
    response.delete_cookie("session")
    return {"message": "Logged out"}


def check_authentication(db, token: str = None) -> dict:
    """Check if user is authenticated based on JWT token"""
    if not token:
        return {"logged_in": False}
    
    try:
        user = get_current_user(db, token)
        return {
            "logged_in": True,
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "name": user.name
            }
        }
    except HTTPException:
        return {"logged_in": False} 