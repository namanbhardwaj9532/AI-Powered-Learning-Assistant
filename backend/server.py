from fastapi import FastAPI, Depends, Form, File, UploadFile
from routes.auth import router as auth_router
from routes.main import router as main_router
from routes.notes import router as notes_router
from routes.chatbot import router as chatbot_router
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

def extract_keywords(content):
    prompt = f"""
Extract the most important keywords and key concepts from the following study material.

Rules:
- Extract only meaningful keywords or concepts.
- Focus on important technical terms, concepts, topics, names, methods, and definitions.
- Do not extract common or generic words.
- Do not include complete sentences.
- Do not include duplicate or closely repeated keywords.
- Keywords must be directly related to the given text.
- Return between 5 and 15 keywords depending on the amount of useful information.
- Return only valid JSON.
- Do not include markdown or any extra text.

Format:

{{
    "keywords": [
        "keyword 1",
        "keyword 2",
        "keyword 3"
    ]
}}

Text:
{content}
"""

    result=groq(prompt)
    return json.loads(result)["keywords"]


def produce_flashcard(keywords, content):

    prompt = f"""
Create flashcards from the following study material.

Keywords:
{keywords}

Rules:
- Generate flashcards based only on the provided study material.
- Use the keywords to identify important concepts.
- The answers must come from the provided study material.
- Do not add information that is not present in the study material.
- Keep questions clear and suitable for revision.
- Keep answers concise but informative.
- Do not create duplicate flashcards.
- Return only valid JSON.
- Do not include markdown or extra text.

Format:

{{
    "flashcards": [
        {{
            "question": "Question here",
            "answer": "Answer here"
        }},
        {{
            "question": "Question here",
            "answer": "Answer here"
        }}
    ]
}}

Study Material:
{content}
"""

    result = groq(prompt)

    return json.loads(result)["flashcards"]

@app.get("/{note_id}/flashcards")
def flashcards(note_id:str):
    object_id=ObjectId(note_id)

    saved_flashcards=flashcards_collection.find_one({
        "note_id":object_id
    })

    if saved_flashcards:
        return {
            "flashcards":saved_flashcards["flashcards"]
        }
    document=list(
        embeddings_collection.find({
            "note_id":object_id
        })
    )

    all_flashcards=[]

    for i in range(0,len(document),10):
        batch=document[i:i+10]
        content="\n\n".join(
            doc["chunk"] for doc in batch
        )

        keyword = extract_keywords(content)

        flashcard=produce_flashcard(keyword,content)

        all_flashcards.extend(flashcard)


    flashcards_collection.insert_one({
        "note_id":object_id,
        "flashcards":all_flashcards
    })
    return {
        "flashcards":all_flashcards
    } 