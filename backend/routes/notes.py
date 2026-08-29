from fastapi import Depends, Form, File, UploadFile, APIRouter
from dependencies.check import get_user
from config.db import notes_collection, embeddings_collection
from config.embedding import embed
from config.groq import groq
from bson import ObjectId
from pypdf import PdfReader
import numpy as np
import os
from uuid import uuid4
from pydantic import BaseModel

router = APIRouter()


@router.get("/notes")
def all_notes(user=Depends(get_user)):
    notes = list(
        notes_collection.find({
            "user_id": user["_id"]
        })
    )

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])

    return notes


def split_text(text, chunk_size=500, overlap=100):
    if not text:
        return []

    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks


@router.post("/notes")
def add_note(
    title: str = Form(...),
    content: str = Form(None),
    file: UploadFile = File(...),
    user=Depends(get_user)
):
    os.makedirs("uploads", exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1]
    new_name = f"{uuid4()}{file_ext}"
    file_path = os.path.join("uploads", new_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    try:
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        total_pages = len(reader.pages)

    except Exception as e:
        return {
            "message": "Failed to read PDF.",
            "error": str(e)
        }

    if not text.strip():
        return {
            "message": "Could not extract text from this PDF."
        }

    chunks = split_text(text)

    if not chunks:
        return {
            "message": "No usable text found in this PDF."
        }

    print(f"PDF contains {len(chunks)} chunks")

    new_note = {
        "user_id": user["_id"],
        "username": user["username"],
        "title": title,
        "content": content,
        "filename": file.filename,
        "filesavedname": new_name,
        "text": text,
        "total_pages": total_pages
    }

    result = notes_collection.insert_one(new_note)
    note_id = result.inserted_id

    print("Creating embeddings...")

    try:
        embeddings = embed(chunks)
    except Exception as e:
        notes_collection.delete_one({
            "_id": note_id
        })

        return {
            "message": "Failed to create embeddings.",
            "error": str(e)
        }

    print("Embeddings created.")

    documents = []

    for i, chunk in enumerate(chunks):
        documents.append({
            "note_id": note_id,
            "chunk_index": i,
            "chunk": chunk,
            "embedding": embeddings[i]
        })

    try:
        if documents:
            embeddings_collection.insert_many(documents)

    except Exception as e:
        notes_collection.delete_one({
            "_id": note_id
        })

        embeddings_collection.delete_many({
            "note_id": note_id
        })

        return {
            "message": "Failed to store embeddings.",
            "error": str(e)
        }

    print("Embeddings stored.")

    notes = list(
        notes_collection.find({
            "user_id": user["_id"]
        })
    )

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])

    return notes


@router.get("/file/{note_id}")
def get_note(note_id: str):
    try:
        object_id = ObjectId(note_id)
    except Exception:
        return {
            "message": "Invalid note ID."
        }

    note = notes_collection.find_one({
        "_id": object_id
    })

    if not note:
        return {
            "message": "Note not found."
        }

    return {
        "title": note["title"],
        "filename": note["filename"],
        "text": note.get("text", ""),
        "tolpages": note.get("total_pages", 0)
    }


class ChatReq(BaseModel):
    prompt: str


@router.post("/{note_id}/chatbot")
def notes_chatbot(
    req: ChatReq,
    note_id: str
):
    print("Question:", req.prompt)

    try:
        object_id = ObjectId(note_id)
    except Exception:
        return {
            "output": "Invalid note ID."
        }

    note = notes_collection.find_one({
        "_id": object_id
    })

    if not note:
        return {
            "output": "Note not found."
        }

    print("Note found.")

    try:
        prompt_embedding = np.array(
            embed([req.prompt])[0],
            dtype=np.float32
        )
    except Exception as e:
        print("Embedding error:", e)

        return {
            "output": "Failed to create an embedding for your question."
        }

    print("Question embedding created.")

    documents = list(
        embeddings_collection.find({
            "note_id": object_id
        })
    )

    print("Chunks retrieved:", len(documents))

    if not documents:
        return {
            "output": "No content found in this note."
        }

    embeddings = np.array(
        [doc["embedding"] for doc in documents],
        dtype=np.float32
    )

    prompt_norm = np.linalg.norm(prompt_embedding)

    if prompt_norm == 0:
        return {
            "output": "Could not process the question."
        }

    prompt_embedding /= prompt_norm

    embedding_norms = np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    embedding_norms[embedding_norms == 0] = 1

    embeddings /= embedding_norms

    similarities = embeddings @ prompt_embedding

    top_k = min(5, len(documents))

    top_indices = np.argsort(
        similarities
    )[-top_k:][::-1]

    top_chunks = [
        documents[index]["chunk"]
        for index in top_indices
    ]

    context = "\n\n".join(top_chunks)

    print("Context created.")

    prompt = f"""
You are an intelligent AI assistant helping the user understand their document.

Use the provided document context as your primary source of information.

Instructions:

- Understand the context instead of simply copying it.
- Explain concepts in your own words.
- Combine information from multiple sections when necessary.
- Answer "what", "why", and "how" questions when the context supports the answer.
- Give examples when they help explain the concept.
- Do not invent information that is not supported by the document.
- If the document does not contain enough information to answer the question,
  clearly say that the information is not available in the provided document.
- Keep the answer clear and useful.

Document context:

{context}

User question:

{req.prompt}

Provide the final answer.
"""

    print("Sending request to Groq...")

    try:
        result = groq(prompt)
    except Exception as e:
        print("Groq error:", e)

        return {
            "output": "Failed to generate an answer."
        }

    print("Groq response received.")

    return {
        "output": result
    }