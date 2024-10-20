# This module is for handling dependencies such as Db connection and other third party
# Integrations.
from pymongo.mongo_client import MongoClient

from .utils import verify_password, get_password_hash
from .config import Config

# connect to db and get connection
def get_db(db_name = "Blog"):
  try:
    # create a client
    client = MongoClient(Config.MONGO_URI)
    return client[db_name]
  except Exception as e:
    raise Exception("Could not connect to the database")
  

# authenticate user
def authenticate_user(username: str, password: str):
  collection = get_db().userInfo
  user = collection.find_one({
    "username" : username
  })
  if not user or not verify_password(password, user["hashed_password"]):
    return False
  
  return user


# To insert admin info into the db. Ran once
if __name__ == "__main__":

  hash_password = get_password_hash("Relativity6#")

  admin_info = {
    "username": "admin",
    "password": "Relativity6#",
    "hashed_password": hash_password
  }

  collection = get_db().userInfo

  result = collection.insert_one(admin_info)

  print(result)
