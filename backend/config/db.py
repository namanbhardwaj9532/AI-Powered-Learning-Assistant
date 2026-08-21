from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("mongo_url")

conn=MongoClient(url)
db=conn["users_db"]
collection=db["users"]

db2=conn["notes_db"]
notes_collection=db2["notes"]

embeddings_collection=db2["embeddings"]
