from fastapi import APIRouter, Cookie, Response
from fastapi.responses import JSONResponse
from services.auth_services import login_user, logout_user, check_authentication

router = APIRouter()


@router.post("/login")
def login(data: dict, response: Response):
    """User login endpoint"""
    return login_user(response, data["username"], data["password"])


@router.post("/logout")
def logout(response: Response):
    """User logout endpoint"""
    return logout_user(response)


@router.get("/check-auth")
def check_auth(session: str = Cookie(None)):
    """Check if user is authenticated"""
    result = check_authentication(session)
    if result["logged_in"]:
        return result
    return JSONResponse(result, status_code=401)
