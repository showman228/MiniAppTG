import secrets
import uuid

from time import time

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = APIRouter(
    prefix="/demo-auth",
    tags=["Demo Auth"]
)

security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password
    }


usernames_to_passwords = {
    "admin": "admin",
    "bob": "1234"
}

static_auth_token_to_username = {
    "85910ce15b9925aaa7b73e868d9e": "john",
    "6626d9b3203a1ff2d228018a2abda9ce0f5e": "admin"
}


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"}
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if not correct_password:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8")
    ):
        raise unauthed_exc

    return credentials.username


def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token")
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid"
    )

    if user := static_auth_token_to_username[static_token]:
        return user

    raise unauthed_exc


@router.get("/basic-auth-username")
def demo_basic_auth_credentials(
    user_username: str = Depends(get_auth_user_username)
):
    return {
        "message": f"Hi! {user_username}",
        "username": user_username,
    }


@router.get("/some-http-header-auth")
def demo_basic_some_http_header(
    user: str = Depends(get_username_by_static_auth_token)
):
    return {
        "username": user,
        "message": f"Hi, {user}!"
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"

def generate_session_id():
    return uuid.uuid4().hex 

def get_session_data(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated"
        )
    return COOKIES[session_id]
    

@router.get("/login-cookie")
def demo_login_set_cookie(
    response: Response,
    auth_username: str = Depends(get_username_by_static_auth_token)
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time())
    }
    
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@router.get("/logout-cookie")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data) 
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}!",
    }


@router.get("/check-cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data) 
):

     username = user_session_data["username"]
     return {
         "message": f"Hello {username}!",
         **user_session_data
     }