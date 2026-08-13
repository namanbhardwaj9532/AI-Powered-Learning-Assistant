from fastapi import FastAPI, Request
from pydantic import BaseModel
from config.db import collection

app=FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def server():
    return {"message":"server running"}

class info(BaseModel):
    username:str
    password:str

@app.post("/register")
def register(user:info):

    existing_user= collection.find_one({
        "username":user.username
    })

    if existing_user:
        return {
            "message":user.username + " is already registered"
        }
    
    user_data={
        "username":user.username,
        "password":user.password
    }
    collection.insert_one(user_data)
    return {
        "message":user.username + " is registered"
    }