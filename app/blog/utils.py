# Utils has all the required functions for different endpoints such as
# hasing incoming password, matching passwords and so on.

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import re
import unicodedata

# Import modules
from .config import Config

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password
def verify_password(plain_password: str, hashed_password : str) -> str:
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password (for adding new users)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

# create URL-friendly URL
def generate_blog_code(value: str) -> str:
    """Convert blog title to a URL-friendly slug."""
      
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value