from fastapi import FastAPI, Depends
from routes.auth import router as auth_router
from routes.main import router as main_router
from pydantic import BaseModel
from config.db import notes_collection
from dependencies.check import get_user


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

app.include_router(auth_router)
app.include_router(main_router)


class Note(BaseModel):
    title:str
    content:str

@app.get("/notes")
def all_notes(user=Depends(get_user)):
    notes=list(notes_collection.find({
        "user_id":user["_id"]
    }))

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])
    return notes


@app.post("/notes")
def add_note(note:Note,
          user=Depends(get_user)):
    new_note={
        "user_id":user["_id"],
        "username":user["username"],
        "title":note.title,
        "content":note.content
    }
    result=notes_collection.insert_one(new_note)
    notes=list(notes_collection.find({
            "user_id":user["_id"]
        }))
    
    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])
    return notes
