# This module is for handling dependencies such as Db connection and other third party
# Integrations.
from pymongo.mongo_client import MongoClient

from .utils import verify_password, get_password_hash
from .schemas import BlogContent, BlogData
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


def combine_content_and_code(blog : BlogContent, blog_code : str) -> BlogData: 

  return BlogData(**blog.model_dump(), url = blog_code)


# retrieve blog informations from db
def get_blog_informations():

  collection = get_db().BlogData

  blogs = collection.find({}, {"_id": 0, "title": 1, "url":1})

  print("data about blogs are ", blogs)

  return {"blog_data": list(blogs)}

  pass

# add blog content to db
def add_blog_to_db(blog: BlogContent, blog_code: str) :

  try:
    # get database
    collection = get_db().BlogData

    data = combine_content_and_code(blog, blog_code)
    print("data is ", data)

    result = collection.insert_one(data.model_dump())

    print("result is ", result.inserted_id)

    return result.inserted_id

  except Exception as e:
    raise Exception(f"DB error : {e}")

  pass
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
