from fastapi import FastAPI, Depends, Form, File, UploadFile, APIRouter
from config.db import notes_collection
from dependencies.check import get_user
import os
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from bson import ObjectId
from pypdf import PdfReader
from config.gemini import embed

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


def split_text(text, chunk_size=500, overlap=100):

    chunks = []
    embeddings=[]

    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        embedding=embed(chunk)
        embeddings.append(embedding)
        chunks.append(chunk)

    return chunks, embeddings

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


    reader=PdfReader(file_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""

    chunks,embeddings=split_text(text)
    new_note = {
        "user_id": user["_id"],
        "username": user["username"],
        "title": title,
        "content": content,
        "filename": file.filename if file else None,
        "filesavedname": new_name,
        "chunks":chunks,
        "embeddings":embeddings
    }

    notes_collection.insert_one(new_note)

    notes = list(notes_collection.find({
        "user_id": user["_id"]
    }))

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])

    return notes




@router.get("/file/{note_id}")
def get_note(note_id: str):

    note = notes_collection.find_one({
        "_id": ObjectId(note_id)
    })

    reader = PdfReader(f"uploads/{note['filesavedname']}")

    tolpage=len(reader.pages)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""


    return {
        "title": note["title"],
        "filename": note["filename"],
        "text": text,
        "tolpages":tolpage
    }