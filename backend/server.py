from fastapi import FastAPI, Depends, Form, File, UploadFile
from routes.auth import router as auth_router
from routes.main import router as main_router
from routes.notes import router as notes_router
from routes.chatbot import router as chatbot_router
from pydantic import BaseModel
from config.db import notes_collection
from dependencies.check import get_user
import os
from bson import ObjectId
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from config.gemini import gemini
from config.groq import groq


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
app.include_router(chatbot_router)

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")

@app.get("/{note_id}/test")
def test(note_id: str):

    object_id = ObjectId(note_id)

    note = notes_collection.find_one({
        "_id": object_id
    })

    if not note:
        return {
            "output": "Note not found."
        }

    content = note["text"]

    prompt = f"""
From the given text, create 5 simple questions.

Rules:
- Questions must be based only on the given text.
- Keep the questions simple.
- Return only the questions.
- Number them from 1 to 5.

Text:
{content}
"""

    result = groq(prompt)

    return {
        "output": result
    }