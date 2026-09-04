from fastapi import FastAPI, Depends, Form, File, UploadFile
from routes.auth import router as auth_router
from routes.main import router as main_router
from routes.notes import router as notes_router
from routes.chatbot import router as chatbot_router
from routes.notes_flashcards import router as flashcards_router
from routes.test import router as test_router
from pydantic import BaseModel
from config.db import notes_collection
from config.db import embeddings_collection
from config.db import quiz_collection
from config.db import flashcards_collection
from dependencies.check import get_user
import os
from bson import ObjectId
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from config.gemini import gemini
from config.groq import groq
import random
import json


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
app.include_router(test_router)
app.include_router(flashcards_router)


