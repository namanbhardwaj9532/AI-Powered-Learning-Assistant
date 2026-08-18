from fastapi import FastAPI, Depends, Form, File, UploadFile, APIRouter
from config.db import notes_collection
from dependencies.check import get_user
import os
from uuid import uuid4
from fastapi.staticfiles import StaticFiles

router=APIRouter()


@router.get("/notes")
def all_notes(user=Depends(get_user)):
    notes=list(notes_collection.find({
        "user_id":user["_id"]
    }))

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])
    return notes


@router.post("/notes")
def add_note(
    title: str = Form(...),
    content: str = Form(None),
    file: UploadFile = File(...),
    user=Depends(get_user)
):
    new_name = None

    if file:
        os.makedirs("uploads", exist_ok=True)

        file_ext = os.path.splitext(file.filename)[1]
        new_name = f"{uuid4()}{file_ext}"

        file_path = os.path.join("uploads", new_name)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

    new_note = {
        "user_id": user["_id"],
        "username": user["username"],
        "title": title,
        "content": content,
        "filename": file.filename if file else None,
        "filesavedname": new_name
    }

    notes_collection.insert_one(new_note)

    notes = list(notes_collection.find({
        "user_id": user["_id"]
    }))

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])

    return notes