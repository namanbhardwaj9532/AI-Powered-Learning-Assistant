from fastapi import FastAPI, Depends, Form, File, UploadFile
from routes.auth import router as auth_router
from routes.main import router as main_router
from routes.notes import router as notes_router
from routes.chatbot import router as chatbot_router
from pydantic import BaseModel
from config.db import notes_collection
from config.db import embeddings_collection
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

app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")

@app.get("/{note_id}/test")
def test(note_id: str):

    object_id = ObjectId(note_id)

    document= list(
        embeddings_collection.find({
            "note_id":object_id
        })
    )

    selected_chunks = random.sample(
        document,
        min(10,len(document))
    )

    content ="\n\n".join(
        doc["chunk"] for doc in selected_chunks
    )

    prompt = f"""
From the given text, create 5 simple questions.

Rules:
- provide mcq type questions
- Questions must be based only on the given text.
- Keep the questions simple.
- Return exactly 5 questions.
- with 4 options for each question
- dont provide answer
- Return only valid JSON.
- Do not include markdown or extra text.

Format:
[
    {{
        "question": "Question 1",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]
    }},
    {{
        "question": "Question 2",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]
    }},
    {{
        "question": "Question 3",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]
    }},
    {{
        "question": "Question 4",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]
    }},
    {{
        "question": "Question 5",
        "options": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]
    }}
]

Text:
{content}
"""

    result = groq(prompt)
    questions=json.loads(result)

    return {
        "questions": questions
    }