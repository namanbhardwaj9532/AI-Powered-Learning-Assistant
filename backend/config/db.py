from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("mongo_url")

conn=MongoClient(url)
db=conn["users_db"]
collection=db["users"]


