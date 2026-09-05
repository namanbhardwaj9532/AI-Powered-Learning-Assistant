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

quiz_collection=db2["quiz"]

flashcards_collection=db2["flashcards"]

testcontent_collection=db2["testcontent"]
testattempts_collection=db2["testattempts"]