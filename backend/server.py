from fastapi import FastAPI, Depends, Form, File, UploadFile
from routes.auth import router as auth_router
from routes.main import router as main_router
from routes.notes import router as notes_router
from pydantic import BaseModel
from config.db import notes_collection
from dependencies.check import get_user
import os
from bson import ObjectId
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader


app=FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")

@app.get("/")
def server():
    return {"message":"server running"}

app.include_router(auth_router)
app.include_router(main_router)
app.include_router(notes_router)

from bson import ObjectId
from pypdf import PdfReader

@app.get("/file/{note_id}")
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