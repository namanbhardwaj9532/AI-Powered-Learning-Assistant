from fastapi import FastAPI, Request, Depends,HTTPException
from bson import ObjectId
from config.db import collection

def get_user(request:Request):
    uid = request._cookies.get("uid")

    if not uid:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id=ObjectId(uid)
    try:
        user=collection.find_one({
                "_id":user_id
            })
    except:
        raise HTTPException(status_code=401, detail="not a registered user")
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user