from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Import functionalities from modules.
from .schemas import Token
from .utils import create_access_token, verify_password, get_password_hash
from .config import Config
from .dependencies import authenticate_user

router = APIRouter()

#OAuth2PasswordBearer sets the endpoint for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint to see the status
@router.get("/")
async def get_status():
    return {"status": "blog router status - OK"}

# Login route to generate token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = authenticate_user(form_data.username, form_data.password)

    print("User is ", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Route to check if token is valid
@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username}

# Endpoint to get the titles of all the blogs
@router.get("/blogs/title")
async def get_blog_titles():
    pass

# Endpoint to get the blog data of a specific blog
@router.get("/blogs/{blog_id}")
async def get_blog(blog_id: int):
    return {"data": blog_id}
