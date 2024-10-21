import os
from dotenv import load_dotenv


load_dotenv()

class Config:
  MONGO_URI = os.getenv("MONGO_URI")
  SECRET_KEY = "mykey"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 300
