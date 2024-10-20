
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_db(db_name ='portalpeek'):
    try:
        # Create a new client and connect to the server
        client = MongoClient(os.getenv("MONGO_URI"))
        # Return the client
        return client[db_name]
    except Exception as e:
        print(e)

db = get_db()
collection = db['announcements']
print(collection)

#CRUD Operations
# 1. Create (Insert)
def create_document(data):
    """Insert a document into the collection."""
    result = collection.insert_one(data)
    print(f"Document inserted with _id: {result.inserted_id}")
    return result.inserted_id

# 2. Read (Find)
def read_document(query):
    """Find a document based on a query."""
    document = collection.find_one(query)
    if document:
        print(f"Document found: {document}")
        return document
    else:
        print("No document matches the query.")
        return None


class Announcement():
    def __init__(self, title, category, topic, description, date, posted_by, _id=None):
        self._id = _id
        self.title = title
        self.category = category
        self.topic = topic
        self.description = description
        self.date = date
        self.posted_by = posted_by

    def save_to_db(self):
        announcement_collection = get_db().announcements

        data = {
            "title": self.title,
            "category": self.category,
            "topic": self.topic,
            "description": self.description,
            "date": self.date,
            "posted_by": self.posted_by
        }

        result = announcement_collection.insert_one(data)

        print("Announcement saved with ID: ", result.inserted_id)

# with open("./announcements.json", "r") as f:
#     data = json.load(f)

#     for date, announcements in data.items():
#         for announcement in announcements:
#             Announcement(**announcement).save_to_db()