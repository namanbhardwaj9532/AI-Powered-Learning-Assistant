from fastapi import APIRouter, Depends, Request
from dependencies.check import get_user
from fastapi.responses import JSONResponse
from config.db import notes_collection,flashcards_collection

router=APIRouter()

@router.get("/main")
def main(user=Depends(get_user)):
    notes = list(
        notes_collection.find({
            "user_id": user["_id"]
        })
    )
    
    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])

    return {"uid":str(user["_id"]),
            "username":user["username"],
            "name":user["name"],
            "email":user["email"],
            "notes":notes}

@router.post("/logout")
def logout(request:Request):
    response=JSONResponse({
        "message":"loged out"
    })
    response.delete_cookie("uid")
    return response

