from fastapi import HTTPException
from .db import get_db
from pydantic import BaseModel


# Models for the user 
class Signup(BaseModel):
    name : str
    email : str
    classOf : int


def validate_user(user : Signup):
    db = get_db()
    user_collection = db['users']

    # Check if email is valid and it is a .nyu email
    if not user.email.endswith("@nyu.edu"):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    # Check if the classOf is valid (between 2010 and 2028)
    if not isinstance(user.classOf, int) or user.classOf < 2010 or user.classOf > 2028:
        raise HTTPException(status_code=400, detail="Invalid class year. Must be between 2010 and 2028")
    
    existing_user = user_collection.find_one({"email": user.email})

    # Check if user already exists
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return True