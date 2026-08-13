from fastapi import APIRouter
from pydantic import BaseModel
from config.db import collection

router=APIRouter()

class info(BaseModel):
    username:str
    password:str

@router.post("/register")
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

@router.post("/login")
def login(user: info):

    existing_user = collection.find_one({
        "username": user.username
    })

    if not existing_user:
        return {
            "message": "wrong credentials"
        }

    if existing_user["password"] != user.password:
        return {
            "message": "wrong password"
        }

    return {
        "message": "login successful"
    }